// Simulated JSON-based authentication system
// In production, this would connect to a real backend

export interface User {
  id: string;
  email: string;
  name: string;
  createdAt: string;
}

interface StoredUser extends User {
  password: string;
}

const STORAGE_KEY = 'ridewise_users';
const SESSION_KEY = 'ridewise_session';

// Initialize with a demo user
const initializeUsers = (): StoredUser[] => {
  const existing = localStorage.getItem(STORAGE_KEY);
  if (existing) {
    return JSON.parse(existing);
  }
  
  const defaultUsers: StoredUser[] = [
    {
      id: '1',
      email: 'demo@ridewise.com',
      password: 'demo123',
      name: 'Demo User',
      createdAt: new Date().toISOString(),
    },
  ];
  
  localStorage.setItem(STORAGE_KEY, JSON.stringify(defaultUsers));
  return defaultUsers;
};

export const signup = async (email: string, password: string, name: string): Promise<{ success: boolean; user?: User; error?: string }> => {
  const users = initializeUsers();
  
  // Check if user already exists
  if (users.find(u => u.email.toLowerCase() === email.toLowerCase())) {
    return { success: false, error: 'An account with this email already exists' };
  }
  
  const newUser: StoredUser = {
    id: Date.now().toString(),
    email: email.toLowerCase(),
    password,
    name,
    createdAt: new Date().toISOString(),
  };
  
  users.push(newUser);
  localStorage.setItem(STORAGE_KEY, JSON.stringify(users));
  
  // Create session
  const { password: _, ...userWithoutPassword } = newUser;
  localStorage.setItem(SESSION_KEY, JSON.stringify(userWithoutPassword));
  
  return { success: true, user: userWithoutPassword };
};

export const login = async (email: string, password: string): Promise<{ success: boolean; user?: User; error?: string }> => {
  const users = initializeUsers();
  
  const user = users.find(
    u => u.email.toLowerCase() === email.toLowerCase() && u.password === password
  );
  
  if (!user) {
    return { success: false, error: 'Invalid email or password' };
  }
  
  const { password: _, ...userWithoutPassword } = user;
  localStorage.setItem(SESSION_KEY, JSON.stringify(userWithoutPassword));
  
  return { success: true, user: userWithoutPassword };
};

export const logout = (): void => {
  localStorage.removeItem(SESSION_KEY);
};

export const getCurrentUser = (): User | null => {
  const session = localStorage.getItem(SESSION_KEY);
  if (!session) return null;
  
  try {
    return JSON.parse(session);
  } catch {
    return null;
  }
};

export const isAuthenticated = (): boolean => {
  return getCurrentUser() !== null;
};
