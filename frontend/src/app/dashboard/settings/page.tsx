'use client';

import { Settings as SettingsIcon, Bell, Shield, Key } from 'lucide-react';
import { useUser } from '@clerk/nextjs';

export default function SettingsPage() {
  const { user } = useUser();

  return (
    <div className="max-w-4xl mx-auto p-8 pb-12">
      <div className="mb-10 mt-2">
        <h1 className="text-3xl font-bold text-white mb-2 flex items-center">
          <SettingsIcon className="mr-3 text-purple-400" size={32} />
          Settings
        </h1>
        <p className="text-slate-400">Configure your application preferences and security settings.</p>
      </div>

      <div className="space-y-6">
        {/* Account Quick Actions */}
        <section className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-lg">
          <h2 className="text-xl font-bold text-white mb-6 flex items-center">
            <Shield className="mr-2 text-indigo-400" size={20} /> Security & Access
          </h2>
          
          <div className="space-y-4">
            <div className="flex items-center justify-between p-4 bg-slate-950 rounded-lg border border-slate-800">
              <div>
                <p className="font-semibold text-white">Change Password</p>
                <p className="text-sm text-slate-400">Update your account password</p>
              </div>
              <button className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-white text-sm font-medium rounded-md transition-colors">
                Manage
              </button>
            </div>

            <div className="flex items-center justify-between p-4 bg-slate-950 rounded-lg border border-slate-800">
              <div>
                <p className="font-semibold text-white">Two-Factor Authentication</p>
                <p className="text-sm text-slate-400">Add an extra layer of security</p>
              </div>
              <span className="px-3 py-1 bg-slate-800 text-slate-400 text-xs font-semibold rounded-full border border-slate-700">
                Managed via Profile
              </span>
            </div>
          </div>
        </section>

        {/* Notifications */}
        <section className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-lg">
          <h2 className="text-xl font-bold text-white mb-6 flex items-center">
            <Bell className="mr-2 text-pink-400" size={20} /> Preferences
          </h2>
          
          <div className="space-y-4">
            <div className="flex items-center justify-between p-4 bg-slate-950 rounded-lg border border-slate-800">
              <div>
                <p className="font-semibold text-white">Email Notifications</p>
                <p className="text-sm text-slate-400">Receive alerts when a scan completes</p>
              </div>
              <label className="relative inline-flex items-center cursor-pointer">
                <input type="checkbox" value="" className="sr-only peer" defaultChecked />
                <div className="w-11 h-6 bg-slate-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-purple-500"></div>
              </label>
            </div>
            
            <div className="flex items-center justify-between p-4 bg-slate-950 rounded-lg border border-slate-800">
              <div>
                <p className="font-semibold text-white">Feature Updates</p>
                <p className="text-sm text-slate-400">News about product enhancements</p>
              </div>
              <label className="relative inline-flex items-center cursor-pointer">
                <input type="checkbox" value="" className="sr-only peer" />
                <div className="w-11 h-6 bg-slate-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-purple-500"></div>
              </label>
            </div>
          </div>
        </section>

        <p className="text-center text-sm text-slate-500 mt-8 pt-8">
          Note: Core identity and password settings are managed through the Profile tab utilizing secure Clerk Authentication.
        </p>
      </div>
    </div>
  );
}
