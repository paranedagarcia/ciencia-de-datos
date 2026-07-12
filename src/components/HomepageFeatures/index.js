import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

const FeatureList = [
  {
    title: 'Comprensión de Datos',
    Svg: require('@site/static/img/undraw_docusaurus_mountain.svg').default,
    description: (
      <>
        Comprender los datos es el primer paso para cualquier proyecto de ciencia de datos. Aquí aprenderás a explorar, limpiar y visualizar datos de manera efectiva.
      </>
    ),
  },
  {
    title: 'Machine Learning',
    Svg: require('@site/static/img/undraw_docusaurus_tree.svg').default,
    description: (
      <>
        El aprendizaje automático permite a las máquinas aprender de los datos y hacer predicciones o decisiones basadas en ellos. Aprenderás los conceptos y técnicas fundamentales de machine learning.

      </>
    ),
  },
  {
    title: 'Producción',
    Svg: require('@site/static/img/undraw_docusaurus_react.svg').default,
    description: (
      <>
        Llevar un proyecto de ciencia de datos a producción implica implementar modelos y soluciones de manera eficiente y escalable. Aprenderás las mejores prácticas para desplegar y mantener tus modelos en un entorno real.
      </>
    ),
  },
];

function Feature({Svg, title, description}) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center">
        <Svg className={styles.featureSvg} role="img" />
      </div>
      <div className="text--center padding-horiz--md">
        <Heading as="h3">{title}</Heading>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
