"use client";

/**
 * Delete Routine Button Component
 * 
 * Wrapper around DeleteButton specifically for routines.
 */

import { useRouter } from "next/navigation";
import DeleteButton from "@/components/common/DeleteButton";
import api from "@/lib/api/client";

interface DeleteRoutineButtonProps {
  routineId: string;
  routineName: string;
}

export default function DeleteRoutineButton({
  routineId,
  routineName,
}: DeleteRoutineButtonProps) {
  const router = useRouter();

  const handleDelete = async () => {
    await api.delete(`/api/routines/${routineId}`);
  };

  return (
    <DeleteButton
      itemName={routineName}
      itemType="Routine"
      onDelete={handleDelete}
      redirectTo="/routines"
    />
  );
}
