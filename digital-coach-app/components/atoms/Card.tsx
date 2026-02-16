import classNames from "classnames";
import { PropsWithChildren } from "react";
import styles from "./Card.module.scss";

interface Props
  extends React.DetailedHTMLProps<
    React.HTMLAttributes<HTMLElement>,
    HTMLElement
  > {
  title?: string;
  multiline?: boolean;
}

export default function Card(props: PropsWithChildren<Props>) {
  const { title, className, multiline, ...rest } = props;

  return (
    <section
      {...rest}
      className={classNames(multiline ? styles.cardMulti : styles.card, className)}>
      {title && <p className={styles.cardTitle}>{title}</p>}
      {props.children}
    </section>
  );
}

