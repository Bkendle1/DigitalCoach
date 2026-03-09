import styles from "./Skeleton.module.scss";

interface Props {
  width?: string;
  height?: string;
}

export default function Skeleton({ width = "100%", height = "20px" }: Props) {
  return (
    <div
      className={styles.skeleton}
      style={{ width, height }}
    />
  );
}