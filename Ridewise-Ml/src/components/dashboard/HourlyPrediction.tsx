import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import {
  Clock,
  Sun,
  Cloud,
  CloudRain,
  Wind,
  CalendarDays,
  Loader2,
  TrendingUp,
  TrendingDown,
  Minus,
  Sparkles,
} from 'lucide-react';
import { predictHourly, HourlyPredictionInput, HourlyPredictionResult } from '@/lib/api';
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';
import { cn } from '@/lib/utils';

const weatherOptions = [
  { value: 'sunny', label: 'Sunny', icon: Sun, color: 'text-amber-500' },
  { value: 'cloudy', label: 'Cloudy', icon: Cloud, color: 'text-gray-400' },
  { value: 'rainy', label: 'Rainy', icon: CloudRain, color: 'text-blue-400' },
  { value: 'windy', label: 'Windy', icon: Wind, color: 'text-cyan-500' },
];

const HourlyPrediction: React.FC = () => {
  const [formData, setFormData] = useState<HourlyPredictionInput>({
    date: new Date().toISOString().split('T')[0],
    hour: new Date().getHours(),
    bikeType: 'yulu',
    weather: 'sunny',
    isEvent: false,
  });
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<HourlyPredictionResult | null>(null);

  const handlePredict = async () => {
    setIsLoading(true);
    const prediction = await predictHourly(formData);
    setResult(prediction);
    setIsLoading(false);
  };

  const getDemandIcon = () => {
    if (!result) return null;
    if (result.demandLevel === 'high') return <TrendingUp className="w-5 h-5 text-primary" />;
    if (result.demandLevel === 'low') return <TrendingDown className="w-5 h-5 text-destructive" />;
    return <Minus className="w-5 h-5 text-amber-500" />;
  };

  const getDemandColor = () => {
    if (!result) return '';
    if (result.demandLevel === 'high') return 'text-primary';
    if (result.demandLevel === 'low') return 'text-destructive';
    return 'text-amber-500';
  };

  return (
    <div className="space-y-8 animate-fade-in">
      <div className="grid lg:grid-cols-2 gap-8">
        {/* Input Form */}
        <div className="glass-card p-6 space-y-6">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center">
              <Clock className="w-5 h-5 text-primary" />
            </div>
            <div>
              <h2 className="text-xl font-bold text-foreground">Hourly Prediction</h2>
              <p className="text-sm text-muted-foreground">Enter parameters to predict demand</p>
            </div>
          </div>

          {/* Date Picker */}
          <div className="space-y-2">
            <Label className="text-foreground flex items-center gap-2">
              <CalendarDays className="w-4 h-4" />
              Select Date
            </Label>
            <input
              type="date"
              value={formData.date}
              onChange={(e) => setFormData({ ...formData, date: e.target.value })}
              className="w-full bg-card border border-border rounded-lg px-4 py-3 text-foreground focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all"
            />
          </div>

          {/* Hour Selector */}
          <div className="space-y-2">
            <Label className="text-foreground flex items-center gap-2">
              <Clock className="w-4 h-4" />
              Select Hour
            </Label>
            <select
              value={formData.hour}
              onChange={(e) => setFormData({ ...formData, hour: parseInt(e.target.value) })}
              className="w-full bg-card border border-border rounded-lg px-4 py-3 text-foreground focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all"
            >
              {Array.from({ length: 24 }, (_, i) => (
                <option key={i} value={i}>
                  {i.toString().padStart(2, '0')}:00 - {i.toString().padStart(2, '0')}:59
                </option>
              ))}
            </select>
          </div>

          {/* Weather */}
          <div className="space-y-2">
            <Label className="text-foreground">Weather Condition</Label>
            <div className="grid grid-cols-4 gap-3">
              {weatherOptions.map((weather) => (
                <button
                  key={weather.value}
                  onClick={() => setFormData({ ...formData, weather: weather.value as any })}
                  className={cn(
                    "flex flex-col items-center gap-2 px-3 py-4 rounded-lg border transition-all duration-200",
                    formData.weather === weather.value
                      ? "border-primary bg-primary/5"
                      : "border-border bg-card hover:border-primary/50"
                  )}
                >
                  <weather.icon className={cn("w-6 h-6", weather.color)} />
                  <span className="text-xs text-foreground">{weather.label}</span>
                </button>
              ))}
            </div>
          </div>

          {/* Event Toggle */}
          <div className="flex items-center justify-between p-4 rounded-lg bg-secondary">
            <div>
              <p className="font-medium text-foreground">Special Event</p>
              <p className="text-sm text-muted-foreground">Is there a local event?</p>
            </div>
            <button
              onClick={() => setFormData({ ...formData, isEvent: !formData.isEvent })}
              className={cn(
                "w-14 h-8 rounded-full transition-all duration-300 relative",
                formData.isEvent ? "bg-primary" : "bg-muted-foreground/30"
              )}
            >
              <div
                className={cn(
                  "w-6 h-6 rounded-full bg-white absolute top-1 transition-all duration-300 shadow-sm",
                  formData.isEvent ? "left-7" : "left-1"
                )}
              />
            </button>
          </div>

          {/* Predict Button */}
          <Button
            variant="hero"
            size="lg"
            className="w-full"
            onClick={handlePredict}
            disabled={isLoading}
          >
            {isLoading ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                Analyzing...
              </>
            ) : (
              <>
                <Sparkles className="w-5 h-5" />
                Predict Demand
              </>
            )}
          </Button>
        </div>

        {/* Results */}
        <div className="space-y-6">
          {result ? (
            <>
              {/* Main Result Card */}
              <div className="glass-card p-6 text-center animate-scale-in">
                <p className="text-sm text-muted-foreground mb-2">Predicted Rentals</p>
                <div className="text-6xl font-bold gradient-text animate-number mb-4">
                  {result.predictedRentals}
                </div>
                <div className="flex items-center justify-center gap-2 mb-4">
                  {getDemandIcon()}
                  <span className={cn("text-lg font-semibold capitalize", getDemandColor())}>
                    {result.demandLevel} Demand
                  </span>
                </div>
                <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-secondary">
                  <span className="text-sm text-muted-foreground">Confidence:</span>
                  <span className="text-sm font-semibold text-primary">{result.confidence}%</span>
                </div>
              </div>

              {/* Recommendation */}
              <div className="glass-card p-6 animate-slide-up" style={{ animationDelay: '0.1s' }}>
                <h4 className="font-semibold text-foreground mb-2">Recommendation</h4>
                <p className="text-muted-foreground">{result.recommendation}</p>
              </div>

              {/* Hourly Breakdown Chart */}
              <div className="glass-card p-6 animate-slide-up" style={{ animationDelay: '0.2s' }}>
                <h4 className="font-semibold text-foreground mb-4">24-Hour Demand Pattern</h4>
                <div className="h-64">
                  <ResponsiveContainer width="100%" height="100%">
                    <AreaChart data={result.hourlyBreakdown}>
                      <defs>
                        <linearGradient id="colorHourly" x1="0" y1="0" x2="0" y2="1">
                          <stop offset="5%" stopColor="hsl(162, 72%, 40%)" stopOpacity={0.3} />
                          <stop offset="95%" stopColor="hsl(162, 72%, 40%)" stopOpacity={0.05} />
                        </linearGradient>
                      </defs>
                      <CartesianGrid strokeDasharray="3 3" stroke="hsl(220, 13%, 91%)" />
                      <XAxis
                        dataKey="hour"
                        stroke="hsl(220, 9%, 46%)"
                        tick={{ fill: 'hsl(220, 9%, 46%)', fontSize: 10 }}
                        tickFormatter={(h) => `${h}:00`}
                      />
                      <YAxis
                        stroke="hsl(220, 9%, 46%)"
                        tick={{ fill: 'hsl(220, 9%, 46%)', fontSize: 10 }}
                      />
                      <Tooltip
                        contentStyle={{
                          backgroundColor: 'hsl(0, 0%, 100%)',
                          border: '1px solid hsl(220, 13%, 91%)',
                          borderRadius: '8px',
                          color: 'hsl(222, 47%, 11%)',
                          boxShadow: '0 4px 12px rgba(0, 0, 0, 0.1)',
                        }}
                        labelFormatter={(h) => `${h}:00`}
                      />
                      <Area
                        type="monotone"
                        dataKey="rentals"
                        stroke="hsl(162, 72%, 40%)"
                        strokeWidth={2}
                        fillOpacity={1}
                        fill="url(#colorHourly)"
                      />
                    </AreaChart>
                  </ResponsiveContainer>
                </div>
              </div>
            </>
          ) : (
            <div className="glass-card p-12 text-center">
              <div className="w-16 h-16 rounded-2xl bg-primary/10 flex items-center justify-center mx-auto mb-4">
                <Clock className="w-8 h-8 text-primary" />
              </div>
              <h3 className="text-xl font-semibold text-foreground mb-2">Ready to Predict</h3>
              <p className="text-muted-foreground">
                Configure the parameters and click "Predict Demand" to see the results.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default HourlyPrediction;
