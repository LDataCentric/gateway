from submodules.model import enums
import pandas as pd
import json


def infer_category(file_name: str) -> str:
    category = file_name.split("_")[-1]
    return (
        enums.RecordCategory.TEST.value
        if enums.RecordCategory.TEST.value.lower() in category.lower()
        else enums.RecordCategory.SCALE.value
    )


def infer_category_enum(df: pd.DataFrame, df_col: str) -> str:
    type_name = df[df_col].dtype.name
    if type_name == "int64":
        return enums.DataTypes.INTEGER.value
    elif type_name == "float64":
        return enums.DataTypes.FLOAT.value
    elif type_name == "bool":
        return enums.DataTypes.BOOLEAN.value
    elif type_name == "object":
        # Check if string is json
        try:
            df[df_col].apply(lambda x: json.loads(x.replace('\'', '"')))
            return enums.DataTypes.TIMESERIES.value
        except Exception:
            pass

        # Extract file extension
        file_extension = df[df_col].apply(lambda x: x.split('.')[-1]).unique()

        audio_inter = list(set(file_extension) & set(enums.FileExtensions.AUDIO_EXTENSIONS.value))
        video_inter = list(set(file_extension) & set(enums.FileExtensions.VIDEO_EXTENSIONS.value))
        image_inter = list(set(file_extension) & set(enums.FileExtensions.IMAGE_EXTENSIONS.value))

        if len(audio_inter) > 0:
            return enums.DataTypes.AUDIO.value
        elif len(video_inter) > 0:
            return enums.DataTypes.VIDEO.value
        elif len(image_inter) > 0:
            return enums.DataTypes.IMAGE.value

        # Check uniqueness of values
        if len(df[df_col].unique()) <= 20:
            return enums.DataTypes.CATEGORY.value

        return enums.DataTypes.TEXT.value

    else:
        return enums.DataTypes.UNKNOWN.value


def infer_category_completeness(df: pd.DataFrame, df_col: str) -> bool:
    return df[df_col].isnull().sum() == 0
