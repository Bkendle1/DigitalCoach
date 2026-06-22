import classNames from "classnames";
import { PropsWithChildren } from "react";
import styles from "./CenteredComponent.module.scss";
interface Props
  extends React.DetailedHTMLProps<
    React.HTMLAttributes<HTMLElement>,
    HTMLElement
  > {
}

export default function CenteredComponent(props: Props) {
    const { className } = props;
  
    return (
      <div className={classNames(styles.centerDiv, className)}>
        {props.children}
      </div>
    );
  }