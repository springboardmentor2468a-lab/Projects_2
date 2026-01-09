import React, { useState } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { User, Mail, Calendar, Shield, Bell, Save, Loader2 } from 'lucide-react';
import { useToast } from '@/hooks/use-toast';
import { cn } from '@/lib/utils';

const Profile: React.FC = () => {
  const { user } = useAuth();
  const { toast } = useToast();
  const [isLoading, setIsLoading] = useState(false);
  const [notifications, setNotifications] = useState({
    email: true,
    push: false,
    weekly: true,
  });

  const handleSave = async () => {
    setIsLoading(true);
    await new Promise((resolve) => setTimeout(resolve, 1000));
    setIsLoading(false);
    toast({
      title: 'Settings saved',
      description: 'Your profile has been updated successfully.',
    });
  };

  return (
    <div className="max-w-3xl mx-auto space-y-8 animate-fade-in">
      {/* Header */}
      <div className="flex items-center gap-4">
        <div className="w-20 h-20 rounded-2xl bg-primary flex items-center justify-center">
          <span className="text-3xl font-bold text-primary-foreground">
            {user?.name?.charAt(0).toUpperCase() || 'U'}
          </span>
        </div>
        <div>
          <h2 className="text-2xl font-bold text-foreground">{user?.name}</h2>
          <p className="text-muted-foreground">{user?.email}</p>
        </div>
      </div>

      {/* Account Information */}
      <div className="glass-card p-6 space-y-6">
        <div className="flex items-center gap-2 mb-2">
          <User className="w-5 h-5 text-primary" />
          <h3 className="text-lg font-semibold text-foreground">Account Information</h3>
        </div>

        <div className="grid md:grid-cols-2 gap-6">
          <div className="space-y-2">
            <Label className="text-foreground">Full Name</Label>
            <Input defaultValue={user?.name} />
          </div>
          <div className="space-y-2">
            <Label className="text-foreground">Email Address</Label>
            <div className="relative">
              <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
              <Input defaultValue={user?.email} className="pl-10" disabled />
            </div>
          </div>
        </div>

        <div className="flex items-center gap-3 p-4 rounded-lg bg-secondary">
          <Calendar className="w-5 h-5 text-muted-foreground" />
          <div>
            <p className="text-sm text-muted-foreground">Member since</p>
            <p className="text-foreground font-medium">
              {user?.createdAt
                ? new Date(user.createdAt).toLocaleDateString('en-US', {
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric',
                  })
                : 'N/A'}
            </p>
          </div>
        </div>
      </div>

      {/* Security */}
      <div className="glass-card p-6 space-y-6">
        <div className="flex items-center gap-2 mb-2">
          <Shield className="w-5 h-5 text-primary" />
          <h3 className="text-lg font-semibold text-foreground">Security</h3>
        </div>

        <div className="space-y-4">
          <div className="flex items-center justify-between p-4 rounded-lg bg-secondary">
            <div>
              <p className="font-medium text-foreground">Password</p>
              <p className="text-sm text-muted-foreground">Last changed 30 days ago</p>
            </div>
            <Button variant="outline" size="sm">
              Change Password
            </Button>
          </div>

          <div className="flex items-center justify-between p-4 rounded-lg bg-secondary">
            <div>
              <p className="font-medium text-foreground">Two-Factor Authentication</p>
              <p className="text-sm text-muted-foreground">Add extra security to your account</p>
            </div>
            <Button variant="outline" size="sm">
              Enable 2FA
            </Button>
          </div>
        </div>
      </div>

      {/* Notifications */}
      <div className="glass-card p-6 space-y-6">
        <div className="flex items-center gap-2 mb-2">
          <Bell className="w-5 h-5 text-primary" />
          <h3 className="text-lg font-semibold text-foreground">Notifications</h3>
        </div>

        <div className="space-y-4">
          {[
            {
              key: 'email',
              title: 'Email Notifications',
              description: 'Receive predictions and insights via email',
            },
            {
              key: 'push',
              title: 'Push Notifications',
              description: 'Get real-time alerts on your device',
            },
            {
              key: 'weekly',
              title: 'Weekly Digest',
              description: 'Summary of weekly analytics and trends',
            },
          ].map((item) => (
            <div
              key={item.key}
              className="flex items-center justify-between p-4 rounded-lg bg-secondary"
            >
              <div>
                <p className="font-medium text-foreground">{item.title}</p>
                <p className="text-sm text-muted-foreground">{item.description}</p>
              </div>
              <button
                onClick={() =>
                  setNotifications((prev) => ({
                    ...prev,
                    [item.key]: !prev[item.key as keyof typeof prev],
                  }))
                }
                className={cn(
                  'w-12 h-7 rounded-full transition-all duration-300 relative',
                  notifications[item.key as keyof typeof notifications]
                    ? 'bg-primary'
                    : 'bg-muted-foreground/30'
                )}
              >
                <div
                  className={cn(
                    'w-5 h-5 rounded-full bg-white absolute top-1 transition-all duration-300 shadow-sm',
                    notifications[item.key as keyof typeof notifications]
                      ? 'left-6'
                      : 'left-1'
                  )}
                />
              </button>
            </div>
          ))}
        </div>
      </div>

      {/* Save Button */}
      <div className="flex justify-end">
        <Button variant="hero" size="lg" onClick={handleSave} disabled={isLoading}>
          {isLoading ? (
            <>
              <Loader2 className="w-5 h-5 animate-spin" />
              Saving...
            </>
          ) : (
            <>
              <Save className="w-5 h-5" />
              Save Changes
            </>
          )}
        </Button>
      </div>
    </div>
  );
};

export default Profile;
