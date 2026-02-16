import classNames from "classnames";
import { forwardRef, InputHTMLAttributes } from "react";

import styles from "./TextField.module.scss";

interface Props extends InputHTMLAttributes<HTMLInputElement> {
  title?: string;
}

export const TextField = forwardRef<HTMLInputElement, Props>(
  ({ title, className, ...props }, ref) => {
    return (
      <div className={classNames(styles.TextField, className)}>
        {title && <label className={styles.TextField_title}>{title}</label>}
        <input ref={ref} className={styles.TextField_input} {...props} />
      </div>
    );
  }
);
TextField.displayName = "TextField";

export default TextField;
