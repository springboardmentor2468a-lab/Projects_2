import React, { useEffect, useState } from 'react';
import { Button } from '@/components/ui/button';
import { Download, Loader2, TrendingUp, Calendar, BarChart3 } from 'lucide-react';
import { getHistoricalData, getWeeklyComparison } from '@/lib/api';
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
  ComposedChart,
  Area,
} from 'recharts';
import { cn } from '@/lib/utils';

const Analytics: React.FC = () => {
  const [historicalData, setHistoricalData] = useState<any[]>([]);
  const [weeklyComparison, setWeeklyComparison] = useState<any[]>([]);
  const [selectedPeriod, setSelectedPeriod] = useState<7 | 14 | 30>(7);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      setIsLoading(true);
      const [historical, weekly] = await Promise.all([
        getHistoricalData(selectedPeriod),
        getWeeklyComparison(),
      ]);
      setHistoricalData(historical);
      setWeeklyComparison(weekly);
      setIsLoading(false);
    };
    fetchData();
  }, [selectedPeriod]);

  const handleExport = () => {
    const csvContent = historicalData
      .map((row) => `${row.date},${Math.round(row.rentals)}`)
      .join('\n');
    const blob = new Blob([`Date,Rentals\n${csvContent}`], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `ridewise-analytics-${selectedPeriod}days.csv`;
    a.click();
  };

  const totalRentals = historicalData.reduce((sum, d) => sum + d.rentals, 0);
  const avgRentals = totalRentals / historicalData.length || 0;
  const maxRentals = Math.max(...historicalData.map((d) => d.rentals), 0);

  return (
    <div className="space-y-8 animate-fade-in">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center">
            <BarChart3 className="w-5 h-5 text-primary" />
          </div>
          <div>
            <h2 className="text-xl font-bold text-foreground">Analytics & Insights</h2>
            <p className="text-sm text-muted-foreground">Historical data visualization</p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          {/* Period Selector */}
          <div className="flex rounded-lg border border-border bg-card p-1">
            {[7, 14, 30].map((days) => (
              <button
                key={days}
                onClick={() => setSelectedPeriod(days as 7 | 14 | 30)}
                className={cn(
                  "px-4 py-2 rounded-md text-sm font-medium transition-all",
                  selectedPeriod === days
                    ? "bg-primary text-primary-foreground"
                    : "text-muted-foreground hover:text-foreground"
                )}
              >
                {days}D
              </button>
            ))}
          </div>

          <Button variant="outline" onClick={handleExport}>
            <Download className="w-4 h-4 mr-2" />
            Export
          </Button>
        </div>
      </div>

      {isLoading ? (
        <div className="glass-card p-12 flex items-center justify-center">
          <Loader2 className="w-8 h-8 animate-spin text-primary" />
        </div>
      ) : (
        <>
          {/* Summary Stats */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div className="stat-card">
              <div className="flex items-center gap-2 mb-2">
                <TrendingUp className="w-4 h-4 text-primary" />
                <span className="text-sm text-muted-foreground">Total Rentals</span>
              </div>
              <p className="text-3xl font-bold text-foreground">{Math.round(totalRentals).toLocaleString()}</p>
            </div>
            <div className="stat-card">
              <div className="flex items-center gap-2 mb-2">
                <Calendar className="w-4 h-4 text-primary" />
                <span className="text-sm text-muted-foreground">Daily Average</span>
              </div>
              <p className="text-3xl font-bold text-foreground">{Math.round(avgRentals).toLocaleString()}</p>
            </div>
            <div className="stat-card">
              <div className="flex items-center gap-2 mb-2">
                <BarChart3 className="w-4 h-4 text-primary" />
                <span className="text-sm text-muted-foreground">Peak Day</span>
              </div>
              <p className="text-3xl font-bold text-foreground">{Math.round(maxRentals).toLocaleString()}</p>
            </div>
          </div>

          {/* Historical Trend Chart */}
          <div className="glass-card p-6">
            <h3 className="text-lg font-semibold text-foreground mb-6">
              Historical Trend ({selectedPeriod} Days)
            </h3>
            <div className="h-80">
              <ResponsiveContainer width="100%" height="100%">
                <ComposedChart data={historicalData}>
                  <defs>
                    <linearGradient id="colorTrend" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="hsl(162, 72%, 40%)" stopOpacity={0.3} />
                      <stop offset="95%" stopColor="hsl(162, 72%, 40%)" stopOpacity={0.05} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="hsl(220, 13%, 91%)" />
                  <XAxis
                    dataKey="dayName"
                    stroke="hsl(220, 9%, 46%)"
                    tick={{ fill: 'hsl(220, 9%, 46%)', fontSize: 12 }}
                  />
                  <YAxis
                    stroke="hsl(220, 9%, 46%)"
                    tick={{ fill: 'hsl(220, 9%, 46%)', fontSize: 12 }}
                  />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: 'hsl(0, 0%, 100%)',
                      border: '1px solid hsl(220, 13%, 91%)',
                      borderRadius: '8px',
                      color: 'hsl(222, 47%, 11%)',
                      boxShadow: '0 4px 12px rgba(0, 0, 0, 0.1)',
                    }}
                  />
                  <Area
                    type="monotone"
                    dataKey="rentals"
                    stroke="hsl(162, 72%, 40%)"
                    strokeWidth={2}
                    fillOpacity={1}
                    fill="url(#colorTrend)"
                  />
                  <Line
                    type="monotone"
                    dataKey="rentals"
                    stroke="hsl(162, 72%, 40%)"
                    strokeWidth={3}
                    dot={{ fill: 'hsl(162, 72%, 40%)', strokeWidth: 0, r: 4 }}
                    activeDot={{ r: 6, fill: 'hsl(152, 76%, 35%)' }}
                  />
                </ComposedChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Weekly Comparison Chart */}
          <div className="glass-card p-6">
            <h3 className="text-lg font-semibold text-foreground mb-6">
              This Week vs Last Week
            </h3>
            <div className="h-80">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={weeklyComparison}>
                  <CartesianGrid strokeDasharray="3 3" stroke="hsl(220, 13%, 91%)" />
                  <XAxis
                    dataKey="day"
                    stroke="hsl(220, 9%, 46%)"
                    tick={{ fill: 'hsl(220, 9%, 46%)', fontSize: 12 }}
                  />
                  <YAxis
                    stroke="hsl(220, 9%, 46%)"
                    tick={{ fill: 'hsl(220, 9%, 46%)', fontSize: 12 }}
                  />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: 'hsl(0, 0%, 100%)',
                      border: '1px solid hsl(220, 13%, 91%)',
                      borderRadius: '8px',
                      color: 'hsl(222, 47%, 11%)',
                      boxShadow: '0 4px 12px rgba(0, 0, 0, 0.1)',
                    }}
                  />
                  <Legend
                    wrapperStyle={{ color: 'hsl(220, 9%, 46%)' }}
                  />
                  <Bar
                    dataKey="thisWeek"
                    name="This Week"
                    fill="hsl(162, 72%, 40%)"
                    radius={[4, 4, 0, 0]}
                  />
                  <Bar
                    dataKey="lastWeek"
                    name="Last Week"
                    fill="hsl(220, 14%, 80%)"
                    radius={[4, 4, 0, 0]}
                  />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Additional Insights */}
          <div className="grid lg:grid-cols-2 gap-6">
            <div className="glass-card p-6">
              <h4 className="font-semibold text-foreground mb-4">Peak Performance Days</h4>
              <div className="space-y-3">
                {historicalData
                  .slice()
                  .sort((a, b) => b.rentals - a.rentals)
                  .slice(0, 3)
                  .map((day, index) => (
                    <div
                      key={day.date}
                      className="flex items-center justify-between p-3 rounded-lg bg-secondary"
                    >
                      <div className="flex items-center gap-3">
                        <div
                          className={cn(
                            "w-8 h-8 rounded-lg flex items-center justify-center font-bold text-sm",
                            index === 0
                              ? "bg-amber-100 text-amber-600"
                              : index === 1
                              ? "bg-gray-100 text-gray-600"
                              : "bg-orange-100 text-orange-600"
                          )}
                        >
                          #{index + 1}
                        </div>
                        <span className="text-foreground">{day.dayName}, {day.date}</span>
                      </div>
                      <span className="font-bold text-primary">{Math.round(day.rentals)}</span>
                    </div>
                  ))}
              </div>
            </div>

            <div className="glass-card p-6">
              <h4 className="font-semibold text-foreground mb-4">Quick Insights</h4>
              <div className="space-y-4">
                <div className="flex items-start gap-3">
                  <div className="w-2 h-2 rounded-full bg-primary mt-2" />
                  <p className="text-muted-foreground">
                    <span className="text-foreground font-medium">Weekend demand</span> is typically{' '}
                    <span className="text-primary font-medium">23% higher</span> than weekdays
                  </p>
                </div>
                <div className="flex items-start gap-3">
                  <div className="w-2 h-2 rounded-full bg-primary mt-2" />
                  <p className="text-muted-foreground">
                    <span className="text-foreground font-medium">Evening rush hours</span> (5-7 PM) see{' '}
                    <span className="text-primary font-medium">maximum utilization</span>
                  </p>
                </div>
                <div className="flex items-start gap-3">
                  <div className="w-2 h-2 rounded-full bg-amber-500 mt-2" />
                  <p className="text-muted-foreground">
                    <span className="text-foreground font-medium">Weather impact:</span> Rainy days show{' '}
                    <span className="text-amber-600 font-medium">45% reduction</span> in rentals
                  </p>
                </div>
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default Analytics;
