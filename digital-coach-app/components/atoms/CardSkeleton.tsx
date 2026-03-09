import Skeleton from "../atoms/Skeleton";

export default function CardSkeleton() {
  return (
    <div>
      <Skeleton height="20px" width="40%" />
      <Skeleton height="40px" width="80%" />
    </div>
  );
}