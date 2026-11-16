import { useState } from "react";
import type { User } from "../types/user";

interface UserProfileCardProps {
  readonly user: User;
  readonly onUpdate?: (user: User) => void;
  readonly className?: string;
}

/**
 * Composant de carte profil utilisateur — présentation pure.
 * Aucune logique de fetching ici. Typage strict des props.
 * Stylé avec Tailwind CSS.
 */
export function UserProfileCard({
  user,
  onUpdate,
  className = "",
}: UserProfileCardProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [fullName, setFullName] = useState(user.fullName);

  const handleSave = () => {
    if (onUpdate && fullName.trim() !== user.fullName) {
      onUpdate({
        ...user,
        fullName: fullName.trim(),
        updatedAt: new Date().toISOString(),
      });
    }
    setIsEditing(false);
  };

  return (
    <article
      className={`rounded-xl border border-slate-200 bg-white p-6 shadow-sm dark:border-slate-700 dark:bg-slate-800 ${className}`}
    >
      <header className="mb-4 flex items-center justify-between">
        <div>
          <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">
            {isEditing ? (
              <input
                type="text"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                className="w-full rounded border border-slate-300 px-2 py-1 text-lg font-semibold dark:border-slate-600 dark:bg-slate-700"
                autoFocus
              />
            ) : (
              user.fullName
            )}
          </h2>
          <p className="text-sm text-slate-500 dark:text-slate-400">{user.email}</p>
        </div>
        <span
          className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${
            user.isActive
              ? "bg-emerald-100 text-emerald-800 dark:bg-emerald-900/30 dark:text-emerald-300"
              : "bg-slate-100 text-slate-800 dark:bg-slate-700 dark:text-slate-300"
          }`}
        >
          {user.isActive ? "Actif" : "Inactif"}
        </span>
      </header>

      <footer className="flex items-center justify-between text-xs text-slate-400">
        <span>ID : {user.id.slice(0, 8)}…</span>
        {onUpdate && (
          <button
            type="button"
            onClick={isEditing ? handleSave : () => setIsEditing(true)}
            className="rounded-md bg-slate-900 px-3 py-1 text-xs font-medium text-white hover:bg-slate-700 dark:bg-slate-100 dark:text-slate-900 dark:hover:bg-slate-200"
          >
            {isEditing ? "Enregistrer" : "Modifier"}
          </button>
        )}
      </footer>
    </article>
  );
}
