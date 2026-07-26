import pandas as pd


class Cleaner:
    """
    Clase encargada de limpiar los distintos reportes exportados desde LinkedIn.

    Cada método recibe un DataFrame correspondiente a un tipo de reporte y
    devuelve uno o varios DataFrames listos para su análisis.
    """

    def _limpiar_columnas(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Normaliza los nombres de las columnas.

        La limpieza consiste en:
        - Eliminar espacios al inicio y final.
        - Convertir a minúsculas.
        - Sustituir espacios por guiones bajos.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame de entrada.

        Returns
        -------
        pd.DataFrame
            DataFrame con nombres de columnas normalizados.
        """
        df = df.copy()

        df.columns = (
            df.columns
            .str.strip()
            .str.lower()
            .str.replace(" ", "_")
        )

        return df

    def _eliminar_duplicados(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Elimina registros duplicados.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame de entrada.

        Returns
        -------
        pd.DataFrame
            DataFrame sin filas duplicadas.
        """
        return df.drop_duplicates()

    def _limpieza_general(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Aplica la limpieza común utilizada en todos los reportes.

        Actualmente realiza:
        - Normalización de nombres de columnas.
        - Eliminación de registros duplicados.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame de entrada.

        Returns
        -------
        pd.DataFrame
            DataFrame limpio.
        """
        df = self._limpiar_columnas(df)
        df = self._eliminar_duplicados(df)

        return df

    def limpiar_descubrimiento(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Limpia el reporte de descubrimiento.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame original exportado desde LinkedIn.

        Returns
        -------
        pd.DataFrame
            DataFrame con el tipo de descubrimiento y el total del intervalo.
        """
        df.columns = ['Tipo', 'Total en intervalo']
        df = self._limpieza_general(df)

        df['tipo'] = (
            df['tipo']
            .astype(str)
            .str.strip()
            .str.lower()
        )

        df['total_en_intervalo'] = df['total_en_intervalo'].astype(int)

        return df

    def limpiar_interaccion(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Limpia el reporte de interacción.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame original exportado desde LinkedIn.

        Returns
        -------
        pd.DataFrame
            DataFrame con las fechas e indicadores correctamente tipados.
        """
        df = self._limpieza_general(df)

        df['fecha'] = pd.to_datetime(df['fecha'], dayfirst=True)
        df['impresiones'] = df['impresiones'].astype(int)
        df['interacciones'] = df['interacciones'].astype(int)

        return df

    def limpiar_publicaciones_principales(
        self,
        df: pd.DataFrame
    ) -> list[pd.DataFrame]:
        """
        Limpia el reporte de publicaciones principales.

        El reporte contiene dos tablas:
        una correspondiente a las publicaciones con mayor número de
        interacciones y otra a las publicaciones con mayor número de
        impresiones.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame original exportado desde LinkedIn.

        Returns
        -------
        list[pd.DataFrame]
            Lista con dos DataFrames:
            - Publicaciones por interacciones.
            - Publicaciones por impresiones.
        """

        # Tabla de publicaciones por interacciones
        df_interacciones = df.iloc[2:, 0:3].copy()
        df_interacciones.columns = [
            'URL de la publicación',
            'Fecha de publicación',
            'Interacciones'
        ]

        df_interacciones = self._limpieza_general(df_interacciones)
        df_interacciones = df_interacciones.dropna()

        df_interacciones['fecha_de_publicación'] = pd.to_datetime(
            df_interacciones['fecha_de_publicación'],
            dayfirst=True
        )

        df_interacciones['interacciones'] = (
            df_interacciones['interacciones']
            .astype(int)
        )

        # Tabla de publicaciones por impresiones
        df_impresiones = df.iloc[2:, 4:].copy()
        df_impresiones.columns = [
            'URL de la publicación',
            'Fecha de publicación',
            'Impresiones'
        ]

        df_impresiones = self._limpieza_general(df_impresiones)
        df_impresiones = df_impresiones.dropna()

        df_impresiones['fecha_de_publicación'] = pd.to_datetime(
            df_impresiones['fecha_de_publicación'],
            dayfirst=True
        )

        df_impresiones['impresiones'] = (
            df_impresiones['impresiones']
            .astype(int)
        )

        return [
            df_interacciones.reset_index(drop=True),
            df_impresiones.reset_index(drop=True)
        ]

    def limpiar_seguidores(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Limpia el reporte de nuevos seguidores.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame original exportado desde LinkedIn.

        Returns
        -------
        pd.DataFrame
            DataFrame con la fecha y el número de nuevos seguidores.
        """
        df = df.iloc[2:, :].copy()
        df.columns = ['Fecha', 'Nuevos seguidores']

        df = self._limpieza_general(df)

        df['fecha'] = pd.to_datetime(df['fecha'], dayfirst=True)
        df['nuevos_seguidores'] = df['nuevos_seguidores'].astype(int)

        return df

    def limpiar_informacion_detallada(
        self,
        df: pd.DataFrame
    ) -> list[tuple[str, pd.DataFrame]]:
        """
        Limpia el reporte de información detallada.

        El reporte contiene distintas categorías (Empresa, Cargo, Sector,
        Ubicación, etc.) en una sola tabla. Este método separa cada categoría
        en un DataFrame independiente.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame original exportado desde LinkedIn.

        Returns
        -------
        list[tuple[str, pd.DataFrame]]
            Lista de tuplas (nombre_categoria, dataframe).
        """
        df = self._limpieza_general(df)

        # Limpiar espacios en columnas de texto
        for col in df.columns:
            if df[col].dtype == object:
                df[col] = (
                    df[col]
                    .astype(str)
                    .str.replace("\xa0", " ", regex=False)
                    .str.strip()
                )

        # Convertir el porcentaje a tipo numérico
        df["porcentaje"] = (
            df["porcentaje"]
            .str.replace("%", "", regex=False)
            .str.replace("< 1", "0.5", regex=False)
            .str.strip()
            .astype(float)
        )

        resultado = []

        # Separar cada categoría en un DataFrame independiente
        for categoria, grupo in df.groupby("información_detallada_principal"):

            tabla = (
                grupo[["valor", "porcentaje"]]
                .reset_index(drop=True)
            )

            resultado.append((categoria, tabla))

        return resultado
