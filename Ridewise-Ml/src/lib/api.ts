// API Service Layer - Ready for ML Backend Integration
// These functions will connect to the actual ML endpoints later

export interface HourlyPredictionInput {
  date: string;
  hour: number;
  bikeType: 'yulu' | 'bounce' | 'electric';
  weather: 'sunny' | 'cloudy' | 'rainy' | 'windy';
  isEvent: boolean;
  temperature?: number;
  humidity?: number;
}

export interface DayWisePredictionInput {
  date: string;
  bikeType: 'yulu' | 'bounce' | 'electric';
  weather: 'sunny' | 'cloudy' | 'rainy' | 'windy';
  isEvent: boolean;
}

export interface HourlyPredictionResult {
  predictedRentals: number;
  confidence: number;
  demandLevel: 'low' | 'medium' | 'high';
  recommendation: string;
  hourlyBreakdown: { hour: number; rentals: number }[];
}

export interface DayWisePredictionResult {
  totalRentals: number;
  peakHourStart: number;
  peakHourEnd: number;
  confidence: number;
  demandLevel: 'low' | 'medium' | 'high';
  utilizationSuggestion: string;
  hourlyDistribution: { hour: number; rentals: number }[];
}

// Simulated API delay
const simulateApiDelay = () => new Promise(resolve => setTimeout(resolve, 1500));

// Generate realistic mock data based on inputs
const generateHourlyData = (hour: number, weather: string, isEvent: boolean) => {
  const baseRentals = {
    sunny: 120,
    cloudy: 90,
    rainy: 40,
    windy: 70,
  }[weather] || 80;

  const hourMultiplier = hour >= 7 && hour <= 9 ? 1.8 : 
                         hour >= 17 && hour <= 19 ? 2.0 :
                         hour >= 12 && hour <= 14 ? 1.4 :
                         hour >= 22 || hour <= 5 ? 0.3 : 1;

  const eventBonus = isEvent ? 1.5 : 1;
  const randomFactor = 0.8 + Math.random() * 0.4;

  return Math.round(baseRentals * hourMultiplier * eventBonus * randomFactor);
};

export const predictHourly = async (input: HourlyPredictionInput): Promise<HourlyPredictionResult> => {
  await simulateApiDelay();

  const rentals = generateHourlyData(input.hour, input.weather, input.isEvent);
  const confidence = 75 + Math.random() * 20;

  const demandLevel: 'low' | 'medium' | 'high' = 
    rentals < 50 ? 'low' : rentals < 120 ? 'medium' : 'high';

  const recommendations = {
    low: 'Low demand expected. Consider promotional offers to boost rentals.',
    medium: 'Moderate demand. Standard bike availability should suffice.',
    high: 'High demand predicted. Ensure maximum fleet availability and consider surge pricing.',
  };

  // Generate 24-hour breakdown
  const hourlyBreakdown = Array.from({ length: 24 }, (_, h) => ({
    hour: h,
    rentals: generateHourlyData(h, input.weather, input.isEvent),
  }));

  return {
    predictedRentals: rentals,
    confidence: Math.round(confidence),
    demandLevel,
    recommendation: recommendations[demandLevel],
    hourlyBreakdown,
  };
};

export const predictDayWise = async (input: DayWisePredictionInput): Promise<DayWisePredictionResult> => {
  await simulateApiDelay();

  const hourlyDistribution = Array.from({ length: 24 }, (_, h) => ({
    hour: h,
    rentals: generateHourlyData(h, input.weather, input.isEvent),
  }));

  const totalRentals = hourlyDistribution.reduce((sum, h) => sum + h.rentals, 0);
  const confidence = 70 + Math.random() * 25;

  const peakHour = hourlyDistribution.reduce((max, curr) => 
    curr.rentals > max.rentals ? curr : max
  );

  const demandLevel: 'low' | 'medium' | 'high' = 
    totalRentals < 800 ? 'low' : totalRentals < 1500 ? 'medium' : 'high';

  const suggestions = {
    low: 'Consider reducing active fleet to optimize operational costs.',
    medium: 'Maintain standard fleet distribution across zones.',
    high: 'Deploy additional bikes to high-traffic zones. Consider partnering with nearby businesses.',
  };

  return {
    totalRentals,
    peakHourStart: Math.max(0, peakHour.hour - 1),
    peakHourEnd: Math.min(23, peakHour.hour + 1),
    confidence: Math.round(confidence),
    demandLevel,
    utilizationSuggestion: suggestions[demandLevel],
    hourlyDistribution,
  };
};

// Historical data for charts
export const getHistoricalData = async (days: number = 7) => {
  await simulateApiDelay();

  return Array.from({ length: days }, (_, i) => {
    const date = new Date();
    date.setDate(date.getDate() - (days - 1 - i));
    
    return {
      date: date.toISOString().split('T')[0],
      rentals: 800 + Math.random() * 800,
      dayName: date.toLocaleDateString('en-US', { weekday: 'short' }),
    };
  });
};

export const getWeeklyComparison = async () => {
  await simulateApiDelay();

  const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
  
  return days.map(day => ({
    day,
    thisWeek: 100 + Math.random() * 150,
    lastWeek: 100 + Math.random() * 150,
  }));
};
