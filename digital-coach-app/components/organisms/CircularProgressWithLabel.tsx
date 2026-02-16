import { Box, CircularProgress, CircularProgressProps, Typography } from "@mui/material";
import styles from "./CircularProgressWithLabel.module.scss";
import classNames from "classnames";

interface Props extends CircularProgressProps {
  value: number; 
  size?: number; 
}

export default function CircularProgressWithLabel({ value, size = 64, className, ...rest }: Props) {
  return (
    <Box className={classNames(styles.circularProgressContainer, className)}>
      <CircularProgress variant="determinate" value={value} size={size} {...rest} />
      <Box className={styles.circularProgressLabel}>
        {`${Math.round(value)}%`}
      </Box>
    </Box>
  );
}
