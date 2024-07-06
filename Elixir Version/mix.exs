defmodule ApkTool.MixProject do
  use Mix.Project

  def project do
    [
      app: :apk_tool,
      version: "0.1.0",
      elixir: "~> 1.12",
      start_permanent: Mix.env() == :prod,
      deps: deps()
    ]
  end

  def application do
    [
      extra_applications: [:logger, :inets]
    ]
  end

  defp deps do
    []
  end
end