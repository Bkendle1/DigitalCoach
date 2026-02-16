import { forwardRef, SelectHTMLAttributes } from "react";
import styles from "./Select.module.scss";

type Props = SelectHTMLAttributes<HTMLSelectElement>;

export const Select = forwardRef<HTMLSelectElement, Props>(
  ({ className, children, ...props }, ref) => (
    <div>
      <select ref={ref} className={className || styles.select} {...props}>
        {children}
      </select>
    </div>
  )
);
Select.displayName = "Select";
