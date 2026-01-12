"use client";

/**
 * Delete Habit Button Component
 * 
 * Wrapper around DeleteButton specifically for habits.
 */

import DeleteButton from "@/components/common/DeleteButton";
import api from "@/lib/api/client";

interface DeleteHabitButtonProps {
  habitId: string;
  habitName: string;
}

export default function DeleteHabitButton({
  habitId,
  habitName,
}: DeleteHabitButtonProps) {
  const handleDelete = async () => {
    await api.delete(`/api/habits/${habitId}`);
  };

  return (
    <DeleteButton
      itemName={habitName}
      itemType="Habit"
      onDelete={handleDelete}
      redirectTo="/habits"
    />
  );
}
