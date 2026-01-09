import React from 'react';
import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Bike, TrendingUp, BarChart3, Zap, ArrowRight, Activity } from 'lucide-react';

const Landing: React.FC = () => {
  return (
    <div className="min-h-screen bg-background overflow-hidden relative">
      {/* Background Elements */}
      <div className="absolute inset-0 bg-grid-pattern bg-[size:60px_60px] opacity-30" />
      <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-primary/5 rounded-full blur-[120px]" />
      <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-primary/5 rounded-full blur-[120px]" />
      
      {/* Navigation */}
      <nav className="relative z-10 container mx-auto px-6 py-6 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-primary flex items-center justify-center">
            <Bike className="w-6 h-6 text-primary-foreground" />
          </div>
          <span className="text-xl font-bold text-foreground">RideWise</span>
        </div>
        
        <div className="flex items-center gap-4">
          <Link to="/login">
            <Button variant="ghost" size="sm">Sign In</Button>
          </Link>
          <Link to="/signup">
            <Button variant="hero" size="sm">Get Started</Button>
          </Link>
        </div>
      </nav>

      {/* Hero Section */}
      <main className="relative z-10 container mx-auto px-6 pt-20 pb-32">
        <div className="max-w-4xl mx-auto text-center">
          {/* Badge */}
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary/10 border border-primary/20 mb-8 animate-fade-in">
            <Zap className="w-4 h-4 text-primary" />
            <span className="text-sm text-primary font-medium">AI-Powered Predictions</span>
          </div>

          {/* Headline */}
          <h1 className="text-5xl md:text-7xl font-bold mb-6 animate-slide-up">
            <span className="text-foreground">Predict Smart.</span>
            <br />
            <span className="gradient-text">Ride Smarter.</span>
          </h1>

          {/* Subheadline */}
          <p className="text-lg md:text-xl text-muted-foreground max-w-2xl mx-auto mb-12 animate-slide-up" style={{ animationDelay: '0.1s' }}>
            Advanced machine learning models to forecast bike rental demand. 
            Optimize your fleet, maximize revenue, and deliver exceptional service.
          </p>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 animate-slide-up" style={{ animationDelay: '0.2s' }}>
            <Link to="/signup">
              <Button variant="hero" size="xl" className="group">
                Start Predicting
                <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </Button>
            </Link>
            <Link to="/login">
              <Button variant="outline" size="xl">
                View Demo
              </Button>
            </Link>
          </div>
        </div>

        {/* Feature Cards */}
        <div className="grid md:grid-cols-3 gap-6 mt-32 max-w-5xl mx-auto">
          {[
            {
              icon: Activity,
              title: 'Hourly Predictions',
              description: 'Real-time demand forecasts for every hour of the day.',
              delay: '0.3s',
            },
            {
              icon: BarChart3,
              title: 'Day-Wise Analysis',
              description: 'Comprehensive daily predictions with peak hour insights.',
              delay: '0.4s',
            },
            {
              icon: TrendingUp,
              title: 'Smart Analytics',
              description: 'Interactive visualizations and historical trend analysis.',
              delay: '0.5s',
            },
          ].map((feature, index) => (
            <div
              key={index}
              className="glass-card-hover p-8 animate-slide-up"
              style={{ animationDelay: feature.delay }}
            >
              <div className="w-14 h-14 rounded-2xl bg-primary/10 flex items-center justify-center mb-6">
                <feature.icon className="w-7 h-7 text-primary" />
              </div>
              <h3 className="text-xl font-semibold text-foreground mb-3">{feature.title}</h3>
              <p className="text-muted-foreground">{feature.description}</p>
            </div>
          ))}
        </div>

        {/* Stats Section */}
        <div className="mt-32 grid grid-cols-2 md:grid-cols-4 gap-8 max-w-4xl mx-auto">
          {[
            { value: '95%', label: 'Prediction Accuracy' },
            { value: '24/7', label: 'Real-time Updates' },
            { value: '50K+', label: 'Daily Predictions' },
            { value: '99.9%', label: 'Uptime' },
          ].map((stat, index) => (
            <div key={index} className="text-center animate-slide-up" style={{ animationDelay: `${0.6 + index * 0.1}s` }}>
              <div className="text-3xl md:text-4xl font-bold gradient-text mb-2">{stat.value}</div>
              <div className="text-sm text-muted-foreground">{stat.label}</div>
            </div>
          ))}
        </div>
      </main>

      {/* Floating bike animation */}
      <div className="absolute bottom-20 right-10 opacity-10 animate-float hidden lg:block">
        <Bike className="w-32 h-32 text-primary" />
      </div>
    </div>
  );
};

export default Landing;
