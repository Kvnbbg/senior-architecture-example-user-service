/**
 * Tests unitaires minimaux du composant UserProfileCard.
 * Utilise React Testing Library + Jest.
 */
import { render, screen, fireEvent } from "@testing-library/react";
import { UserProfileCard } from "../components/UserProfileCard";
import type { User } from "../types/user";
import { toUserId } from "../types/user";

const mockUser: User = {
  id: toUserId("123e4567-e89b-12d3-a456-426614174000"),
  email: "test@example.com",
  fullName: "Jean Dupont",
  isActive: true,
  createdAt: new Date().toISOString(),
  updatedAt: new Date().toISOString(),
};

describe("UserProfileCard", () => {
  it("affiche le nom et l'email de l'utilisateur", () => {
    render(<UserProfileCard user={mockUser} />);
    expect(screen.getByText("Jean Dupont")).toBeInTheDocument();
    expect(screen.getByText("test@example.com")).toBeInTheDocument();
  });

  it("affiche le badge Actif", () => {
    render(<UserProfileCard user={mockUser} />);
    expect(screen.getByText("Actif")).toBeInTheDocument();
  });

  it("passe en mode édition et appelle onUpdate", () => {
    const onUpdate = jest.fn();
    render(<UserProfileCard user={mockUser} onUpdate={onUpdate} />);

    fireEvent.click(screen.getByRole("button", { name: "Modifier" }));
    const input = screen.getByDisplayValue("Jean Dupont");
    fireEvent.change(input, { target: { value: "Jean Martin" } });
    fireEvent.click(screen.getByRole("button", { name: "Enregistrer" }));

    expect(onUpdate).toHaveBeenCalledTimes(1);
    expect(onUpdate.mock.calls[0][0].fullName).toBe("Jean Martin");
  });
});
