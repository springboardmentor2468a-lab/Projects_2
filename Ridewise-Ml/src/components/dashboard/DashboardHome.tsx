import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '@/contexts/AuthContext';
import { Button } from '@/components/ui/button';
import {
  TrendingUp,
  TrendingDown,
  Clock,
  Calendar,
  Sun,
  Cloud,
  Bike,
  ArrowRight,
  Loader2,
} from 'lucide-react';
import { getHistoricalData, getWeeklyComparison } from '@/lib/api';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  AreaChart,
  Area,
} from 'recharts';

const DashboardHome: React.FC = () => {
  const { user } = useAuth();
  const [historicalData, setHistoricalData] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      const data = await getHistoricalData(7);
      setHistoricalData(data);
      setIsLoading(false);
    };
    fetchData();
  }, []);

  const today = new Date().toLocaleDateString('en-US', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });

  const stats = [
    {
      label: 'Estimated Today',
      value: '1,247',
      change: '+12.5%',
      trend: 'up',
      icon: Bike,
    },
    {
      label: 'Peak Hour',
      value: '6:00 PM',
      change: 'Rush hour',
      trend: 'neutral',
      icon: Clock,
    },
    {
      label: 'Demand Trend',
      value: 'High',
      change: '+8.2%',
      trend: 'up',
      icon: TrendingUp,
    },
    {
      label: "Weekly Avg",
      value: '1,089',
      change: '-2.1%',
      trend: 'down',
      icon: Calendar,
    },
  ];

  return (
    <div className="space-y-8 animate-fade-in">
      {/* Welcome Section */}
      <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold text-foreground mb-1">
            Welcome back, {user?.name?.split(' ')[0]}!
          </h2>
          <p className="text-muted-foreground">{today}</p>
        </div>
        <div className="flex items-center gap-3">
          <div className="glass-card px-4 py-2 flex items-center gap-2">
            <Sun className="w-5 h-5 text-amber-500" />
            <span className="text-sm text-foreground">Sunny, 28°C</span>
          </div>
          <div className="glass-card px-4 py-2 flex items-center gap-2">
            <Cloud className="w-5 h-5 text-muted-foreground" />
            <span className="text-sm text-foreground">Low humidity</span>
          </div>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {stats.map((stat, index) => (
          <div
            key={stat.label}
            className="stat-card animate-slide-up"
            style={{ animationDelay: `${index * 0.1}s` }}
          >
            <div className="flex items-start justify-between mb-4">
              <div className="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center">
                <stat.icon className="w-6 h-6 text-primary" />
              </div>
              <div
                className={`flex items-center gap-1 text-sm ${
                  stat.trend === 'up'
                    ? 'text-primary'
                    : stat.trend === 'down'
                    ? 'text-destructive'
                    : 'text-muted-foreground'
                }`}
              >
                {stat.trend === 'up' && <TrendingUp className="w-4 h-4" />}
                {stat.trend === 'down' && <TrendingDown className="w-4 h-4" />}
                <span>{stat.change}</span>
              </div>
            </div>
            <h3 className="text-3xl font-bold text-foreground mb-1">{stat.value}</h3>
            <p className="text-sm text-muted-foreground">{stat.label}</p>
          </div>
        ))}
      </div>

      {/* Quick Actions & Chart */}
      <div className="grid lg:grid-cols-3 gap-6">
        {/* Quick Actions */}
        <div className="space-y-4">
          <h3 className="text-lg font-semibold text-foreground">Quick Actions</h3>
          <div className="space-y-3">
            <Link to="/dashboard/hourly" className="block">
              <div className="glass-card-hover p-4 flex items-center justify-between group">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center">
                    <Clock className="w-5 h-5 text-primary" />
                  </div>
                  <div>
                    <p className="font-medium text-foreground">Hourly Prediction</p>
                    <p className="text-sm text-muted-foreground">Predict by hour</p>
                  </div>
                </div>
                <ArrowRight className="w-5 h-5 text-muted-foreground group-hover:text-primary group-hover:translate-x-1 transition-all" />
              </div>
            </Link>

            <Link to="/dashboard/daywise" className="block">
              <div className="glass-card-hover p-4 flex items-center justify-between group">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center">
                    <Calendar className="w-5 h-5 text-primary" />
                  </div>
                  <div>
                    <p className="font-medium text-foreground">Day-Wise Prediction</p>
                    <p className="text-sm text-muted-foreground">Full day analysis</p>
                  </div>
                </div>
                <ArrowRight className="w-5 h-5 text-muted-foreground group-hover:text-primary group-hover:translate-x-1 transition-all" />
              </div>
            </Link>
          </div>
        </div>

        {/* Weekly Chart */}
        <div className="lg:col-span-2 glass-card p-6">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-lg font-semibold text-foreground">Weekly Trend</h3>
            <div className="flex items-center gap-4 text-sm">
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full bg-primary" />
                <span className="text-muted-foreground">Rentals</span>
              </div>
            </div>
          </div>

          {isLoading ? (
            <div className="h-64 flex items-center justify-center">
              <Loader2 className="w-8 h-8 animate-spin text-primary" />
            </div>
          ) : (
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={historicalData}>
                  <defs>
                    <linearGradient id="colorRentals" x1="0" y1="0" x2="0" y2="1">
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
                    fill="url(#colorRentals)"
                  />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default DashboardHome;
