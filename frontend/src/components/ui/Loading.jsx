import { cn } from "@/lib/utils";

export function Loading({ className, size = 20, text = "Loading..." }) {
  return (
    <div className={cn("flex flex-col items-center justify-center space-y-4", className)}>
      {/* Large Animated Loader */}
      <div className="relative flex items-center justify-center">
        <div
          className={`w-${size} h-${size} border-[6px] border-gray-300 border-t-black rounded-full 
                      animate-spin shadow-lg`}
        ></div>

        {/* Inner Soft Glow */}
        <div className="absolute w-2/3 h-2/3 bg-black rounded-full opacity-10 blur-2xl"></div>
      </div>

      {/* Subtle Animated Text */}
      <p className="text-lg font-semibold text-gray-800 animate-pulse">{text}</p>
    </div>
  );
}
