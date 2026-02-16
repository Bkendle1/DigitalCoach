import classNames from "classnames";
import { ButtonHTMLAttributes, DetailedHTMLProps } from "react";
import styles from "./Button.module.scss";

interface Props
  extends DetailedHTMLProps<
    ButtonHTMLAttributes<HTMLButtonElement>,
    HTMLButtonElement
  > {}

export default function Button(props: Props) {
  const { className, ...rest } = props;
  return (
    <button 
    {...rest} className={classNames(styles.button, className)}>
      {props.children}
    </button>
  );
}
