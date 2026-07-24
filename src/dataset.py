import pandas as pd


class Dataset:
    """
    Representa un libro de Excel donde cada hoja se almacena como un DataFrame.

    La clase permite cargar todas las hojas del archivo, obtener la lista de
    hojas disponibles, acceder a un DataFrame específico y actualizar su
    contenido durante el flujo de procesamiento.
    """

    def __init__(self, ruta: str) -> None:
        """
        Inicializa el conjunto de datos a partir de un archivo de Excel.

        Parameters
        ----------
        ruta : str
            Ruta del archivo de Excel.
        """
        self.ruta: str = ruta

        # Diccionario donde:
        #   llave -> nombre de la hoja
        #   valor -> DataFrame correspondiente
        self.data: dict[str, pd.DataFrame] = pd.read_excel(
            ruta,
            sheet_name=None
        )

        # Lista con los nombres de las hojas del archivo.
        self.hojas: list[str] = list(self.data.keys())

    def obtener_hojas(self) -> list[str]:
        """
        Devuelve los nombres de todas las hojas del archivo.

        Returns
        -------
        list[str]
            Lista con los nombres de las hojas.
        """
        return self.hojas

    def obtener_df(self, hoja: str) -> pd.DataFrame | None:
        """
        Obtiene el DataFrame asociado a una hoja.

        Parameters
        ----------
        hoja : str
            Nombre de la hoja.

        Returns
        -------
        pd.DataFrame | None
            DataFrame correspondiente si la hoja existe;
            en caso contrario, devuelve None.
        """
        return self.data.get(hoja)

    def actualizar_df(self, hoja: str, df: pd.DataFrame) -> None:
        """
        Reemplaza el DataFrame asociado a una hoja.

        Parameters
        ----------
        hoja : str
            Nombre de la hoja.
        df : pd.DataFrame
            Nuevo DataFrame que sustituirá al actual.
        """
        self.data[hoja] = df
