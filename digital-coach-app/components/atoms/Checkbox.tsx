import classNames from "classnames";
import React from "react";
import styles from "./Checkbox.module.scss";

export interface CheckBoxProps
  extends React.DetailedHTMLProps<
    React.InputHTMLAttributes<HTMLInputElement>,
    HTMLInputElement
  > {}

export default function Checkbox({ className, ...props }: CheckBoxProps) {
  return (
    <input {...props} type="checkbox" className={classNames(styles.checkbox, className)} />
  );
}
