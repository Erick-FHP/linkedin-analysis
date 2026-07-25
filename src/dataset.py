import pandas as pd


class Dataset:
    """
    Representa un libro de Excel donde cada hoja se almacena como un DataFrame.
    """

    def __init__(self, ruta: str) -> None:
        """
        Inicializa el conjunto de datos a partir de un archivo de Excel.

        Parameters
        ----------
        ruta : str
            Ruta del archivo de Excel.
        """
        self.ruta = ruta

        # Diccionario:
        #   llave -> nombre de la hoja
        #   valor -> DataFrame correspondiente
        self.data: dict[str, pd.DataFrame] = pd.read_excel(
            ruta,
            sheet_name=None
        )

    def obtener_hojas(self) -> list[str]:
        """
        Devuelve los nombres de todas las hojas.
        """
        return list(self.data.keys())

    def obtener_df(self, hoja: str) -> pd.DataFrame | None:
        """
        Obtiene el DataFrame asociado a una hoja.
        """
        return self.data.get(hoja)

    def agregar_df(self, hoja: str, df: pd.DataFrame) -> None:
        """
        Agrega una nueva hoja al conjunto de datos.

        Parameters
        ----------
        hoja : str
            Nombre de la nueva hoja.
        df : pd.DataFrame
            DataFrame asociado.

        Raises
        ------
        KeyError
            Si la hoja ya existe.
        """
        if hoja in self.data:
            raise KeyError(f"La hoja '{hoja}' ya existe.")

        self.data[hoja] = df

    def actualizar_df(self, hoja: str, df: pd.DataFrame) -> None:
        """
        Actualiza el DataFrame de una hoja existente.

        Parameters
        ----------
        hoja : str
            Nombre de la hoja.
        df : pd.DataFrame
            Nuevo DataFrame.

        Raises
        ------
        KeyError
            Si la hoja no existe.
        """
        if hoja not in self.data:
            raise KeyError(f"La hoja '{hoja}' no existe.")

        self.data[hoja] = df

    def eliminar_df(self, hoja: str) -> None:
        """
        Elimina una hoja del conjunto de datos.

        Parameters
        ----------
        hoja : str
            Nombre de la hoja.

        Raises
        ------
        KeyError
            Si la hoja no existe.
        """
        if hoja not in self.data:
            raise KeyError(f"La hoja '{hoja}' no existe.")

        del self.data[hoja]
