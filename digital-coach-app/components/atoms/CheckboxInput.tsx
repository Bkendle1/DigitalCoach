import { PropsWithChildren } from "react";
import Checkbox, { CheckBoxProps } from "./Checkbox";
import styles from "./CheckboxInput.module.scss";

interface Props extends CheckBoxProps {}

export default function CheckboxField(props: PropsWithChildren<Props>) {
  const { children, ...checkboxProps } = props;

  return (
    <label className={styles.checkboxField}>
      <Checkbox {...checkboxProps} />
      <span className={styles.label}>{children}</span>
    </label>
  );
}
