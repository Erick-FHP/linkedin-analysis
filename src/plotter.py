import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns


class Plotter:
    """
    Clase encargada de generar gráficas con un estilo oscuro minimalista.
    """

    def __init__(self) -> None:

        # ========= Tamaño =========

        self.figsize = (10, 6)
        self.dpi = 150

        # ========= Colores =========

        self.background = "#111111"
        self.axes_background = "#1A1A1A"

        self.text = "#ECECEC"

        self.grid = "#444444"

        self.primary = "#00E5FF"
        self.success = "#00FF9F"
        self.warning = "#FFD60A"
        self.danger = "#FF5C5C"

        self.palette = [
            self.primary,
            self.success,
            self.warning,
            self.danger,
            "#C77DFF",
            "#4D96FF",
            "#FF9F1C",
            "#2EC4B6",
        ]

        self._configurar_estilo()

    # =====================================================
    # Configuración
    # =====================================================

    def _configurar_estilo(self):

        plt.style.use("dark_background")

        sns.set_theme(
            style="ticks",
            palette=self.palette
        )

        plt.rcParams.update({

            "figure.figsize": self.figsize,
            "figure.dpi": self.dpi,

            "figure.facecolor": self.background,
            "axes.facecolor": self.axes_background,

            "text.color": self.text,
            "axes.labelcolor": self.text,
            "axes.titlecolor": self.text,
            "xtick.color": self.text,
            "ytick.color": self.text,

            "axes.edgecolor": self.axes_background,

            "grid.color": self.grid,
            "grid.linestyle": "--",
            "grid.alpha": 0.35,

            "font.size": 11,
            "axes.titlesize": 16,
            "axes.labelsize": 12,

            "legend.frameon": False,

        })

    # =====================================================
    # Utilidades
    # =====================================================

    def _formatear_numero(self, x, pos):

        if x >= 1_000_000:
            return f"{x/1_000_000:.1f}M"

        if x >= 1_000:
            return f"{x/1_000:.1f}K"

        return f"{int(x)}"

    def _finalizar(
        self,
        ax,
        titulo,
        xlabel="",
        ylabel="",
        formato_x=True,
        formato_y=True
    ):

        ax.set_title(
            titulo,
            pad=18,
            weight="bold"
        )

        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)

        ax.grid(True)

        if formato_x:
            ax.xaxis.set_major_formatter(
                mticker.FuncFormatter(self._formatear_numero)
            )

        if formato_y:
            ax.yaxis.set_major_formatter(
                mticker.FuncFormatter(self._formatear_numero)
            )

        sns.despine()

        plt.tight_layout()

    # =====================================================
    # Gráficas
    # =====================================================

    def lineplot(
        self,
        data,
        x,
        y,
        titulo,
        hue=None,
        color=None,
        marker="o"
    ):

        fig, ax = plt.subplots()

        sns.lineplot(
            data=data,
            x=x,
            y=y,
            hue=hue,
            marker=marker,
            linewidth=2.5,
            palette=self.palette if hue else None,
            color=color if hue is None else None,
            ax=ax
        )

        self._finalizar(ax, titulo, x, y, formato_x=False)

        return fig, ax

    def barplot(
        self,
        data,
        x,
        y,
        titulo,
        color=None
    ):

        fig, ax = plt.subplots()

        sns.barplot(
            data=data,
            x=x,
            y=y,
            color=color or self.primary,
            ax=ax
        )

        self._finalizar(ax, titulo, x, y, formato_x=False)

        plt.xticks(rotation=45)

        return fig, ax

    def horizontal_barplot(
        self,
        data,
        x,
        y,
        titulo,
        color=None
    ):

        fig, ax = plt.subplots()

        sns.barplot(
            data=data,
            x=x,
            y=y,
            color=color or self.primary,
            orient="h",
            ax=ax
        )

        self._finalizar(ax, titulo, x, y)

        return fig, ax

    def scatterplot(
        self,
        data,
        x,
        y,
        titulo,
        color=None
    ):

        fig, ax = plt.subplots()

        sns.scatterplot(
            data=data,
            x=x,
            y=y,
            s=90,
            color=color or self.primary,
            ax=ax
        )

        self._finalizar(ax, titulo, x, y)

        return fig, ax

    def histplot(
        self,
        data,
        x,
        titulo,
        bins=20,
        color=None
    ):

        fig, ax = plt.subplots()

        sns.histplot(
            data=data,
            x=x,
            bins=bins,
            kde=True,
            color=color or self.primary,
            ax=ax
        )

        self._finalizar(
            ax,
            titulo,
            x,
            "Frecuencia"
        )

        return fig, ax

    def distributionplot(
        self,
        data,
        titulo,
        color=None
    ):
        """
        Grafica una distribución categórica ordenada por porcentaje.

        Parameters
        ----------
        data : pd.DataFrame
            DataFrame con las columnas 'valor' y 'porcentaje'.
        titulo : str
            Título de la gráfica.
        color : str | None, optional
            Color de las barras.
        """

        data = data.sort_values(
            "porcentaje",
            ascending=True
        )

        fig, ax = plt.subplots()

        sns.barplot(
            data=data,
            x="porcentaje",
            y="valor",
            color=color or self.primary,
            ax=ax
        )

        self._finalizar(
            ax,
            titulo,
            xlabel="Porcentaje (%)",
            ylabel="",
            formato_y=False
        )

        ax.xaxis.set_major_formatter(
            mticker.PercentFormatter(xmax=100)
        )

        return fig, ax

    # =====================================================
    # Exportar
    # =====================================================

    def guardar(
        self,
        fig,
        ruta,
        dpi=300
    ):

        fig.savefig(
            ruta,
            dpi=dpi,
            bbox_inches="tight",
            facecolor=self.background
        )
