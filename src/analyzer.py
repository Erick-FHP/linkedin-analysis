import pandas as pd

from dataset import Dataset


class Analyzer:
    """
    Clase encargada de realizar el análisis de los distintos reportes de
    LinkedIn.

    Cada método devuelve un diccionario con las métricas calculadas a partir
    de una hoja del Dataset.
    """

    def __init__(self, dataset: Dataset) -> None:
        """
        Inicializa el analizador.

        Parameters
        ----------
        dataset : Dataset
            Dataset con todos los reportes ya limpios.
        """
        self.dataset = dataset

    def _obtener_hoja(self, hoja: str) -> pd.DataFrame:
        """
        Obtiene un DataFrame del Dataset.

        Parameters
        ----------
        hoja : str
            Nombre de la hoja.

        Returns
        -------
        pd.DataFrame
            DataFrame correspondiente.

        Raises
        ------
        ValueError
            Si la hoja no existe.
        """
        df = self.dataset.obtener_df(hoja)

        if df is None:
            raise ValueError(f"No existe la hoja '{hoja}'.")

        return df

    def analizar_descubrimiento(self) -> dict:
        """
        Analiza el reporte de descubrimiento.

        Calcula las métricas generales relacionadas con el alcance e
        impresiones del contenido.

        Returns
        -------
        dict
            Diccionario con las métricas calculadas.
        """

        df = self.dataset.obtener_df("DESCUBRIMIENTO")

        if df is None:
            raise ValueError("No existe la hoja 'DESCUBRIMIENTO'.")

        # Obtener métricas principales
        impresiones = (
            df.loc[
                df["tipo"] == "impresiones",
                "total_en_intervalo"
            ]
            .iloc[0]
        )

        miembros = (
            df.loc[
                df["tipo"] == "miembros alcanzados",
                "total_en_intervalo"
            ]
            .iloc[0]
        )

        return {
            "tabla": df,
            "impresiones": impresiones,
            "miembros_alcanzados": miembros,
            "impresiones_por_miembro": impresiones / miembros
            if miembros > 0 else None
        }

    def analizar_interacciones(self) -> dict:
        """
        Analiza el reporte de interacción.

        Returns
        -------
        dict
            Diccionario con las métricas calculadas.
        """

        df = self._obtener_hoja("INTERACCIÓN")

        return {
            "tabla": df,
            "total_impresiones": df["impresiones"].sum(),
            "total_interacciones": df["interacciones"].sum(),
            "promedio_impresiones": df["impresiones"].mean(),
            "promedio_interacciones": df["interacciones"].mean(),
            "max_impresiones": df["impresiones"].max(),
            "max_interacciones": df["interacciones"].max(),
            "fecha_max_impresiones": df.loc[
                df["impresiones"].idxmax(),
                "fecha"
            ],
            "fecha_max_interacciones": df.loc[
                df["interacciones"].idxmax(),
                "fecha"
            ]
        }

    def analizar_seguidores(self) -> dict:
        """
        Analiza el reporte de seguidores.

        Returns
        -------
        dict
            Diccionario con las métricas calculadas.
        """

        df = self._obtener_hoja("SEGUIDORES")

        return {
            "tabla": df,
            "total_nuevos_seguidores": df["nuevos_seguidores"].sum(),
            "promedio_diario": df["nuevos_seguidores"].mean(),
            "max_nuevos_seguidores": df["nuevos_seguidores"].max(),
            "fecha_max_nuevos_seguidores": df.loc[
                df["nuevos_seguidores"].idxmax(),
                "fecha"
            ],
            "dias_con_crecimiento": (df["nuevos_seguidores"] > 0).sum(),
            "dias_sin_crecimiento": (df["nuevos_seguidores"] == 0).sum()
        }

    def analizar_principales_interacciones(self) -> dict:
        """
        Analiza las publicaciones con mayor número de interacciones.
        """

        df = self._obtener_hoja("PRINCIPALES INTERACCIONES")

        return {
            "tabla": df,
            "total_interacciones": df["interacciones"].sum(),
            "promedio_interacciones": df["interacciones"].mean(),
            "max_interacciones": df["interacciones"].max(),
            "publicacion_top": df.loc[
                df["interacciones"].idxmax(),
                "url_de_la_publicación"
            ],
            "fecha_top": df.loc[
                df["interacciones"].idxmax(),
                "fecha_de_publicación"
            ]
        }

    def analizar_principales_impresiones(self) -> dict:
        """
        Analiza las publicaciones con mayor número de impresiones.
        """

        df = self._obtener_hoja("PRINCIPALES IMPRESIONES")

        return {
            "tabla": df,
            "total_impresiones": df["impresiones"].sum(),
            "promedio_impresiones": df["impresiones"].mean(),
            "max_impresiones": df["impresiones"].max(),
            "publicacion_top": df.loc[
                df["impresiones"].idxmax(),
                "url_de_la_publicación"
            ],
            "fecha_top": df.loc[
                df["impresiones"].idxmax(),
                "fecha_de_publicación"
            ]
        }

    def analizar_publicaciones(self) -> dict:
        """
        Analiza conjuntamente las publicaciones principales.
        """

        interacciones = self._obtener_hoja("PRINCIPALES INTERACCIONES")
        impresiones = self._obtener_hoja("PRINCIPALES IMPRESIONES")

        df = (
            interacciones
            .merge(
                impresiones,
                on=[
                    "url_de_la_publicación",
                    "fecha_de_publicación"
                ],
                how="outer"
            )
            .fillna(0)
        )

        df["interacciones_por_impresion"] = (
            df["interacciones"] / df["impresiones"]
        )

        return {
            "tabla": df,
            "publicacion_mayor_engagement":
                df.loc[
                    df["interacciones_por_impresion"].idxmax(),
                    "url_de_la_publicación"
                ],
            "engagement_maximo":
                df["interacciones_por_impresion"].max(),
            "correlacion":
                df["interacciones"].corr(df["impresiones"])
        }

    def analizar_distribucion(
        self,
        hoja: str,
        top: int | None = None
    ) -> dict:
        """
        Analiza una distribución categórica.

        Parameters
        ----------
        hoja : str
            Nombre de la hoja.
        top : int | None, optional
            Número máximo de categorías a conservar.

        Returns
        -------
        dict
            Diccionario con el DataFrame listo para visualizar.
        """

        df = self._obtener_hoja(hoja).copy()

        df = df.sort_values(
            "porcentaje",
            ascending=False
        )

        if top is not None:
            df = df.head(top)

        return {
            "tabla": df.reset_index(drop=True),
            "categorias": len(df),
            "porcentaje_total": df["porcentaje"].sum()
        }
