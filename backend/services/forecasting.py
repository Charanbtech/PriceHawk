# backend/services/forecasting.py
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class ForecastingService:
    def __init__(self):
        self.prophet_available = False
        try:
            from prophet import Prophet
            self.Prophet = Prophet
            self.prophet_available = True
        except ImportError:
            logger.warning("Prophet not available, using simple forecasting")

    def forecast_price(self, product_id: str, days_ahead: int = 7):
        """Generate price forecast using Prophet or simple trend analysis"""
        try:
            # Get historical price data (mock for now)
            historical_data = self._get_mock_historical_data(product_id, days=30)
            
            if self.prophet_available and len(historical_data) >= 10:
                return self._prophet_forecast(historical_data, days_ahead, product_id)
            else:
                return self._simple_forecast(historical_data, days_ahead, product_id)
                
        except Exception as e:
            logger.error(f"Forecasting error: {str(e)}")
            return self._demo_forecast(product_id, days_ahead)

    def _demo_forecast(self, product_id: str, days_ahead: int):
        """Demo forecast when real forecasting fails"""
        base_price = 500 + abs(hash(product_id)) % 500
        predictions = []
        
        for i in range(1, days_ahead + 1):
            future_date = (datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d')
            predicted_price = base_price * (0.98 + 0.02 * np.random.random())
            
            predictions.append({
                "date": future_date,
                "predicted_price": round(predicted_price, 2),
                "lower_bound": round(predicted_price * 0.95, 2),
                "upper_bound": round(predicted_price * 1.05, 2),
                "confidence": "demo"
            })
        
        return {
            "status": "success",
            "model": "demo",
            "product_id": product_id,
            "current_price": base_price,
            "predictions": predictions,
            "trend": "decreasing",
            "recommendation": f"💡 Demo: Price expected to drop by 2-3% in next {days_ahead} days"
        }

    def _prophet_forecast(self, historical_data, days_ahead, product_id):
        """Use Facebook Prophet for advanced forecasting"""
        try:
            # Prepare data for Prophet
            df = pd.DataFrame(historical_data)
            df['ds'] = pd.to_datetime(df['date'])
            df['y'] = df['price']
            
            # Initialize Prophet with seasonality
            model = self.Prophet(
                daily_seasonality=False,
                weekly_seasonality=True,
                yearly_seasonality=False,
                changepoint_prior_scale=0.05
            )
            
            # Add custom seasonalities for sales events
            model.add_seasonality(name='monthly', period=30.5, fourier_order=5)
            
            # Fit the model
            model.fit(df[['ds', 'y']])
            
            # Create future dataframe
            future = model.make_future_dataframe(periods=days_ahead)
            forecast = model.predict(future)
            
            # Extract forecast results
            future_forecast = forecast.tail(days_ahead)
            
            predictions = []
            for _, row in future_forecast.iterrows():
                predictions.append({
                    "date": row['ds'].strftime('%Y-%m-%d'),
                    "predicted_price": round(max(0, row['yhat']), 2),
                    "lower_bound": round(max(0, row['yhat_lower']), 2),
                    "upper_bound": round(row['yhat_upper'], 2),
                    "confidence": "high" if abs(row['yhat_upper'] - row['yhat_lower']) < row['yhat'] * 0.1 else "medium"
                })
            
            # Calculate trend
            current_price = historical_data[-1]['price']
            avg_predicted = np.mean([p['predicted_price'] for p in predictions])
            trend = "increasing" if avg_predicted > current_price else "decreasing"
            
            return {
                "status": "success",
                "model": "prophet",
                "product_id": product_id,
                "current_price": current_price,
                "predictions": predictions,
                "trend": trend,
                "recommendation": self._generate_recommendation(current_price, predictions, trend)
            }
            
        except Exception as e:
            logger.error(f"Prophet forecasting failed: {str(e)}")
            return self._simple_forecast(historical_data, days_ahead, product_id)

    def _simple_forecast(self, historical_data, days_ahead, product_id):
        """Simple trend-based forecasting as fallback"""
        try:
            prices = [item['price'] for item in historical_data]
            dates = [item['date'] for item in historical_data]
            
            # Calculate simple trend
            if len(prices) >= 3:
                recent_trend = np.mean(np.diff(prices[-7:]))  # Last 7 days trend
                overall_trend = (prices[-1] - prices[0]) / len(prices)
                trend_weight = 0.7 * recent_trend + 0.3 * overall_trend
            else:
                trend_weight = 0
            
            current_price = prices[-1]
            predictions = []
            
            for i in range(1, days_ahead + 1):
                # Add some randomness and seasonal effects
                seasonal_factor = 1 + 0.05 * np.sin(2 * np.pi * i / 7)  # Weekly pattern
                noise = np.random.normal(0, current_price * 0.02)  # 2% noise
                
                predicted_price = current_price + (trend_weight * i * seasonal_factor) + noise
                predicted_price = max(0, predicted_price)  # Ensure positive price
                
                future_date = datetime.strptime(dates[-1], '%Y-%m-%d') + timedelta(days=i)
                
                predictions.append({
                    "date": future_date.strftime('%Y-%m-%d'),
                    "predicted_price": round(predicted_price, 2),
                    "lower_bound": round(predicted_price * 0.95, 2),
                    "upper_bound": round(predicted_price * 1.05, 2),
                    "confidence": "medium"
                })
            
            trend = "increasing" if trend_weight > 0 else "decreasing"
            
            return {
                "status": "success",
                "model": "simple_trend",
                "product_id": product_id,
                "current_price": current_price,
                "predictions": predictions,
                "trend": trend,
                "recommendation": self._generate_recommendation(current_price, predictions, trend)
            }
            
        except Exception as e:
            logger.error(f"Simple forecasting failed: {str(e)}")
            return self._demo_forecast(product_id, days_ahead)

    def _generate_recommendation(self, current_price, predictions, trend):
        """Generate buying recommendation based on forecast"""
        if not predictions:
            return "Insufficient data for recommendation"
        
        avg_future_price = np.mean([p['predicted_price'] for p in predictions])
        price_change_pct = ((avg_future_price - current_price) / current_price) * 100
        
        if trend == "decreasing" and price_change_pct < -5:
            return f"💡 Wait to buy - Price expected to drop by {abs(price_change_pct):.1f}% in next {len(predictions)} days"
        elif trend == "increasing" and price_change_pct > 5:
            return f"🚀 Buy now - Price expected to rise by {price_change_pct:.1f}% in next {len(predictions)} days"
        else:
            return f"📊 Stable pricing - Price change expected: {price_change_pct:+.1f}%"

    def _get_mock_historical_data(self, product_id: str, days: int = 30):
        """Generate mock historical price data"""
        base_price = 500 + abs(hash(product_id)) % 1000  # Deterministic base price
        data = []
        
        for i in range(days):
            date = (datetime.now() - timedelta(days=days-i)).strftime('%Y-%m-%d')
            
            # Add trends and seasonality
            trend = -0.5 * i  # Slight downward trend
            seasonal = 20 * np.sin(2 * np.pi * i / 7)  # Weekly pattern
            noise = np.random.normal(0, 10)  # Random noise
            
            price = base_price + trend + seasonal + noise
            price = max(50, price)  # Minimum price
            
            data.append({
                "date": date,
                "price": round(price, 2)
            })
        
        return data

    def get_historical_analysis(self, product_id: str):
        """Get historical price analysis"""
        try:
            historical_data = self._get_mock_historical_data(product_id, days=90)
            prices = [item['price'] for item in historical_data]
            
            analysis = {
                "product_id": product_id,
                "period_days": len(historical_data),
                "current_price": prices[-1],
                "min_price": min(prices),
                "max_price": max(prices),
                "avg_price": round(np.mean(prices), 2),
                "price_volatility": round(np.std(prices), 2),
                "price_trend": "decreasing" if prices[-1] < prices[0] else "increasing",
                "best_price_date": historical_data[prices.index(min(prices))]['date'],
                "savings_opportunity": round(prices[-1] - min(prices), 2)
            }
            
            return {"status": "success", "analysis": analysis}
            
        except Exception as e:
            logger.error(f"Historical analysis failed: {str(e)}")
            return {"error": "Analysis failed", "message": str(e)}