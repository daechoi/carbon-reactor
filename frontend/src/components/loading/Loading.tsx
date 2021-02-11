import loadingSvg from './loading.svg'
import styles from './Loading.module.scss'

export const Loading: React.FC<{ isLoading: boolean }> = ({ isLoading }) =>
  isLoading ? <img src={loadingSvg} className={styles.loading} alt="Loading..." /> : <></>
