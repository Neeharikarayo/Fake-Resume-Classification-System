'use client';

import { UserProfile } from "@clerk/nextjs";
import { dark } from "@clerk/themes";

/**
 * Custom styled Clerk UserProfile component matching the AI SaaS dark theme (slate-950).
 * Matches aesthetics of OpenAI, Vercel, and Stripe.
 */
const CustomUserProfile = () => {
  return (
    <div className="flex justify-center w-full py-12">
      <UserProfile
        appearance={{
          baseTheme: dark,
          variables: {
            colorPrimary: "#4f46e5", // indigo-600
            colorBackground: "#0f172a", // slate-900
            colorInputBackground: "#1e293b", // slate-800
            colorInputText: "#ffffff",
            colorText: "#f8fafc", // slate-50
            colorTextSecondary: "#94a3b8", // slate-400
            colorDanger: "#ef4444", // red-500
          },
          elements: {
            card: "bg-slate-900 border border-slate-800 rounded-2xl shadow-xl",
            headerTitle: "text-white text-2xl font-bold",
            headerSubtitle: "text-slate-400",
            profileSectionTitle: "text-white font-semibold border-b border-slate-800 pb-2",
            profileSectionContent: "text-slate-300",
            formButtonPrimary: "bg-indigo-600 hover:bg-indigo-500 text-white shadow-md transition-all rounded-lg font-medium",
            formButtonReset: "text-slate-300 hover:bg-slate-800 hover:text-white transition-colors",
            formFieldLabel: "text-slate-300 font-medium",
            formFieldInput: "bg-slate-800 text-white border-slate-700 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 rounded-lg",
            footerActionText: "text-slate-400",
            navbarButton: "text-slate-400 hover:text-white hover:bg-slate-800 transition-colors rounded-lg",
            navbarButton__active: "text-white bg-slate-800",
            profilePage: "bg-slate-900",
            badge: "bg-slate-800 text-slate-300 border border-slate-700",
            dividerRow: "border-slate-800",
            dividerLine: "bg-slate-800",
            userPreviewSecondaryIdentifier: "text-slate-400",
            userPreviewMainIdentifier: "text-white font-semibold",
            scrollBox: "scrollbar-thin scrollbar-thumb-slate-700 scrollbar-track-transparent",
            profileSectionPrimaryButton: "text-indigo-400 hover:text-indigo-300 hover:bg-indigo-500/10 transition-colors",
            avatarImageActionsUpload: "text-indigo-400 hover:text-indigo-300",
            actionCard: "bg-slate-900 border border-slate-800 shadow-md",
            pageScrollBox: "bg-slate-900",
            navbar: "bg-slate-900/50 border-r border-slate-800",
            breadcrumbsItem: "text-slate-400 hover:text-white",
            breadcrumbsItemDivider: "text-slate-600",
            menuButton: "text-slate-400 hover:text-white",
          }
        }}
      />
    </div>
  );
};

export default CustomUserProfile;
