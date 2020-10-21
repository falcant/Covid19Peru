a few things to do before running the script:

1. make sure you install the following packages (open the anaconda promt cmd)

  - conda install -c conda-forge ffmpeg-python
  - pip install bar_chart_race (or conda install -c conda-forge bar_chart_race)

2 . These 2 links will help

  - https://pypi.org/project/bar-chart-race/    (to see an example of how the barchar race is being applied)

  - ffmpeg for python (https://anaconda.org/conda-forge/ffmpeg-python)


3. make sure that you change your Date feature (column) to a date format
   - using pandas: for example, if the date feature in your data set is called 'pgm_start_date', then do this

   - df['pgm_start_date'] = pd.to_datetime(df['pgm_start_date'])        

    - the "df" stands for the name of your dataframe and "pd" is part of the pandas package.