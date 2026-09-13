export function ErrorState({ message }: { message: string }) {
  return (
    <div className="empty-state error-state">
      <strong>Unable to load data</strong>
      <span>{message}</span>
    </div>
  );
}
