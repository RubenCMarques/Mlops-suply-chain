export default function Status({ tone = 'neutral', children }) {
  return <span className={`status status-${tone}`}><i aria-hidden="true" />{children}</span>;
}
