defmodule ApkTool do
  @apktool_dir "bin"
  @original_dir "1.Original_File"
  @decompile_dir "2.Decomple_File"
  @recompile_dir "3.Recomple_File"

  @apktool_jar_url "bin/apktool.jar"
  @apktool_bat_url "bin/apktool.bat"
  
  @apktool_jar_path Path.join(@apktool_dir, "apktool.jar")
  @apktool_bat_path Path.join(@apktool_dir, "apktool.bat")

  def download_file(url, dest_path) do
    unless File.exists?(dest_path) do
      IO.puts("Downloading #{url} to #{dest_path} ...")
      case HTTPoison.get(url) do
        {:ok, response} ->
          File.write!(dest_path, response.body)
          IO.puts("File #{dest_path} downloaded successfully.")
        {:error, reason} ->
          IO.puts("Failed to download file: #{reason}")
      end
    end
  end

  def decompile_apk(apk_file) do
    apk_name = Path.basename(apk_file, ".apk")
    output_dir = Path.join(@decompile_dir, apk_name)
    unless File.dir?(output_dir) do
      File.mkdir_p!(output_dir)
    end

    IO.puts("Starting decompile of #{apk_file}...")
    {output, exit_code} = System.cmd(@apktool_bat_path, ["d", apk_file, "-o", output_dir, "-f"], stderr_to_stdout: true)
    IO.puts(output)
    if exit_code == 0 do
      IO.puts("File #{apk_file} decompiled successfully.")
    else
      IO.puts("Failed to decompile file #{apk_file}.")
    end
  end

  def recompile_apk(decompiled_dir) do
    apk_name = Path.basename(decompiled_dir)
    output_file = Path.join(@recompile_dir, "#{apk_name}.apk")

    IO.puts("Starting recompile of #{decompiled_dir}...")
    {output, exit_code} = System.cmd(@apktool_bat_path, ["b", decompiled_dir, "-o", output_file], stderr_to_stdout: true)
    IO.puts(output)
    if exit_code == 0 do
      IO.puts("Folder #{decompiled_dir} recompiled successfully.")
    else
      IO.puts("Failed to recompile folder #{decompiled_dir}.")
    end
  end

  def print_ascii_art do
    ascii_art = """
	
	
    =================================================
    Title   : Apktools - Decompiled & Recompiled Apk
    Version : 1.0 (Elixir)
    Site    : https://i-as.dev
    Github  : https://github.com/fitri-hy/apktool
    Creator : Fitri HY
    =================================================
    """
    IO.puts(ascii_art)
  end

  def main_menu do
    print_ascii_art()
    loop()
  end

  defp loop do
    apk_files = Enum.filter(File.ls!(@original_dir), fn f -> String.ends_with?(f, ".apk") end)

    IO.puts("Select an action:")
    IO.puts("1. Decompile APK")
    IO.puts("2. Recompile APK")
    IO.puts("3. Exit")
    action = IO.gets("> ") |> String.trim() |> String.to_integer()

    case action do
      1 ->
        if apk_files == [] do
          IO.puts("APK file is not available in the #{@original_dir} folder.")
        else
          IO.puts("Select APK file to decompile:")
          apk_files
          |> Enum.with_index(1)
          |> Enum.each(fn {file, index} -> IO.puts("#{index}. #{file}") end)
          choice = IO.gets("> ") |> String.trim() |> String.to_integer()
          selected_apk = Enum.at(apk_files, choice - 1)

          Task.async(fn ->
            decompile_apk(Path.join(@original_dir, selected_apk))
          end)
          |> Task.await(:infinity)
        end
        loop()

      2 ->
        decompiled_dirs = Enum.filter(File.ls!(@decompile_dir), fn f -> File.dir?(Path.join(@decompile_dir, f)) end)
        if decompiled_dirs == [] do
          IO.puts("APK file is not available in the #{@decompile_dir} folder.")
        else
          IO.puts("Select decompiled results to recompile:")
          decompiled_dirs
          |> Enum.with_index(1)
          |> Enum.each(fn {dir, index} -> IO.puts("#{index}. #{dir}") end)
          choice = IO.gets("> ") |> String.trim() |> String.to_integer()
          selected_decompiled_dir = Enum.at(decompiled_dirs, choice - 1)

          Task.async(fn ->
            recompile_apk(Path.join(@decompile_dir, selected_decompiled_dir))
          end)
          |> Task.await(:infinity)
        end
        loop()

      3 ->
        IO.puts("Exit the program.")
        :ok

      _ ->
        IO.puts("Invalid choice, please select again.")
        loop()
    end
  end

  def run do
    File.mkdir_p!(@apktool_dir)
    File.mkdir_p!(@original_dir)
    File.mkdir_p!(@decompile_dir)
    File.mkdir_p!(@recompile_dir)

    download_file(@apktool_jar_url, @apktool_jar_path)
    download_file(@apktool_bat_url, @apktool_bat_path)

    main_menu()
  end
end

ApkTool.run()
