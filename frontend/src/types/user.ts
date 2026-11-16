/**
 * Types TypeScript stricts et étanches pour le domaine User.
 * Branded types pour éviter les confusions d'identifiants.
 */

/** Identifiant unique fortement typé */
export type UserId = string & { readonly __brand: "UserId" };

export interface User {
  readonly id: UserId;
  readonly email: string;
  readonly fullName: string;
  readonly isActive: boolean;
  readonly createdAt: string; // ISO 8601
  readonly updatedAt: string;
}

export interface UserCreatePayload {
  readonly email: string;
  readonly fullName: string;
  readonly isActive?: boolean;
}

export interface UserUpdatePayload {
  readonly email?: string;
  readonly fullName?: string;
  readonly isActive?: boolean;
}

/** Utilitaire pour créer un UserId brandé (à utiliser après validation) */
export function toUserId(id: string): UserId {
  return id as UserId;
}
