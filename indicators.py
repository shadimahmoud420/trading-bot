# 📊 مكتبة حساب المؤشرات الفنية
# Technical Indicators Calculation Library

import numpy as np
import pandas as pd
from typing import Dict, Tuple

class TechnicalIndicators:
    """فئة شاملة لحساب جميع المؤشرات الفنية"""
    
    @staticmethod
    def calculate_rsi(prices: np.ndarray, period: int = 14) -> float:
        """
        حساب مؤشر القوة النسبية (RSI)
        RSI = 100 - (100 / (1 + RS))
        RS = Average Gain / Average Loss
        """
        if len(prices) < period + 1:
            return None
        
        deltas = np.diff(prices)
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)
        
        avg_gain = np.mean(gains[-period:])
        avg_loss = np.mean(losses[-period:])
        
        if avg_loss == 0:
            return 100 if avg_gain > 0 else 50
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    @staticmethod
    def calculate_macd(prices: np.ndarray, fast: int = 12, slow: int = 26, 
                       signal: int = 9) -> Tuple[float, float, float]:
        """
        حساب MACD (Moving Average Convergence Divergence)
        MACD = EMA12 - EMA26
        Signal Line = EMA9 من MACD
        Histogram = MACD - Signal
        """
        if len(prices) < slow:
            return None, None, None
        
        ema_fast = TechnicalIndicators.calculate_ema(prices, fast)
        ema_slow = TechnicalIndicators.calculate_ema(prices, slow)
        
        if ema_fast is None or ema_slow is None:
            return None, None, None
        
        macd = ema_fast - ema_slow
        signal_line = TechnicalIndicators.calculate_ema(
            np.array([macd]), signal
        )
        histogram = macd - (signal_line if signal_line else macd)
        
        return macd, signal_line, histogram
    
    @staticmethod
    def calculate_ema(prices: np.ndarray, period: int) -> float:
        """حساب المتوسط المتحرك الأسي (EMA)"""
        if len(prices) < period:
            return None
        
        multiplier = 2 / (period + 1)
        ema = np.mean(prices[:period])
        
        for price in prices[period:]:
            ema = price * multiplier + ema * (1 - multiplier)
        
        return ema
    
    @staticmethod
    def calculate_sma(prices: np.ndarray, period: int) -> float:
        """حساب المتوسط المتحرك البسيط (SMA)"""
        if len(prices) < period:
            return None
        return np.mean(prices[-period:])
    
    @staticmethod
    def calculate_bollinger_bands(prices: np.ndarray, period: int = 20, 
                                 std_dev: float = 2) -> Tuple[float, float, float]:
        """
        حساب Bollinger Bands
        Middle Band = SMA
        Upper Band = SMA + (std_dev × STD)
        Lower Band = SMA - (std_dev × STD)
        """
        if len(prices) < period:
            return None, None, None
        
        middle = np.mean(prices[-period:])
        std = np.std(prices[-period:])
        
        upper = middle + (std_dev * std)
        lower = middle - (std_dev * std)
        
        return upper, middle, lower
    
    @staticmethod
    def calculate_stochastic(prices: np.ndarray, high: np.ndarray, 
                            low: np.ndarray, period: int = 14) -> Tuple[float, float]:
        """
        حساب Stochastic Oscillator
        %K = ((Close - Low) / (High - Low)) × 100
        %D = SMA of %K
        """
        if len(prices) < period:
            return None, None
        
        lowest_low = np.min(low[-period:])
        highest_high = np.max(high[-period:])
        
        if highest_high == lowest_low:
            return 50, 50
        
        k = ((prices[-1] - lowest_low) / (highest_high - lowest_low)) * 100
        
        return k, k  # مبسط - في الواقع D يكون SMA من K
    
    @staticmethod
    def analyze_all_indicators(prices: np.ndarray, highs: np.ndarray, 
                               lows: np.ndarray) -> Dict:
        """تحليل شامل لجميع المؤشرات وإرجاع النتائج"""
        
        result = {
            "timestamp": pd.Timestamp.now(),
            "current_price": prices[-1],
            "indicators": {},
            "signals": {}
        }
        
        # RSI
        rsi = TechnicalIndicators.calculate_rsi(prices, 14)
        result["indicators"]["RSI"] = rsi
        if rsi is not None:
            if rsi > 70:
                result["signals"]["RSI"] = "OVERBOUGHT"  # بيع
            elif rsi < 30:
                result["signals"]["RSI"] = "OVERSOLD"  # شراء
            else:
                result["signals"]["RSI"] = "NEUTRAL"
        
        # MACD
        macd, signal, hist = TechnicalIndicators.calculate_macd(prices, 12, 26, 9)
        result["indicators"]["MACD"] = macd
        result["indicators"]["MACD_Signal"] = signal
        result["indicators"]["MACD_Histogram"] = hist
        if macd is not None and signal is not None:
            if macd > signal:
                result["signals"]["MACD"] = "BUY"
            elif macd < signal:
                result["signals"]["MACD"] = "SELL"
            else:
                result["signals"]["MACD"] = "NEUTRAL"
        
        # Bollinger Bands
        upper, middle, lower = TechnicalIndicators.calculate_bollinger_bands(
            prices, 20, 2
        )
        result["indicators"]["BB_Upper"] = upper
        result["indicators"]["BB_Middle"] = middle
        result["indicators"]["BB_Lower"] = lower
        if upper is not None:
            price = prices[-1]
            if price > upper:
                result["signals"]["Bollinger"] = "OVERBOUGHT"
            elif price < lower:
                result["signals"]["Bollinger"] = "OVERSOLD"
            else:
                result["signals"]["Bollinger"] = "NEUTRAL"
        
        # EMA
        ema_20 = TechnicalIndicators.calculate_ema(prices, 20)
        ema_50 = TechnicalIndicators.calculate_ema(prices, 50)
        result["indicators"]["EMA_20"] = ema_20
        result["indicators"]["EMA_50"] = ema_50
        if ema_20 is not None and ema_50 is not None:
            if ema_20 > ema_50:
                result["signals"]["EMA"] = "BUY"
            else:
                result["signals"]["EMA"] = "SELL"
        
        # Stochastic
        k, d = TechnicalIndicators.calculate_stochastic(prices, highs, lows, 14)
        result["indicators"]["Stochastic_K"] = k
        result["indicators"]["Stochastic_D"] = d
        if k is not None:
            if k > 80:
                result["signals"]["Stochastic"] = "OVERBOUGHT"
            elif k < 20:
                result["signals"]["Stochastic"] = "OVERSOLD"
            else:
                result["signals"]["Stochastic"] = "NEUTRAL"
        
        return result

class MoneyManagement:
    """فئة إدارة رأس المال وحساب نقاط الدخول والخروج"""
    
    @staticmethod
    def calculate_position_size(account_balance: float, risk_percentage: float = 0.03,
                               entry_price: float = 0, stop_loss: float = 0) -> Dict:
        """
        حساب حجم العقد بناءً على إدارة رأس المال
        Position Size = (Account × Risk%) / (Entry - Stop Loss) pips
        """
        risk_amount = account_balance * risk_percentage
        
        if entry_price > 0 and stop_loss > 0:
            pips_risk = abs(entry_price - stop_loss)
            position_size = risk_amount / pips_risk if pips_risk > 0 else 0
        else:
            position_size = 0
        
        return {
            "account_balance": account_balance,
            "risk_amount": risk_amount,
            "risk_percentage": risk_percentage,
            "position_size": position_size,
            "entry_price": entry_price,
            "stop_loss": stop_loss
        }
    
    @staticmethod
    def calculate_tp_sl(current_price: float, signal: str, atr: float = None) -> Dict:
        """
        حساب Take Profit و Stop Loss
        للشراء: SL = Current - ATR, TP = Current + (ATR × 2)
        للبيع: SL = Current + ATR, TP = Current - (ATR × 2)
        """
        if atr is None:
            atr = current_price * 0.01  # 1% كـ default ATR
        
        if signal == "BUY":
            stop_loss = current_price - atr
            take_profit = current_price + (atr * 2)
            risk_reward = 2.0
        elif signal == "SELL":
            stop_loss = current_price + atr
            take_profit = current_price - (atr * 2)
            risk_reward = 2.0
        else:
            return None
        
        return {
            "signal": signal,
            "entry": current_price,
            "stop_loss": stop_loss,
            "take_profit": take_profit,
            "risk_reward_ratio": risk_reward,
            "risk_pips": abs(current_price - stop_loss),
            "reward_pips": abs(take_profit - current_price)
        }
