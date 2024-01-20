import ee
import pandas as pd


def filter_time_roi(roi_geom, image_collection, start_date, end_date):
    
    filt_time = ee.Filter.date(start_date, end_date)
    filt_roi = ee.Filter.bounds(
        ee.FeatureCollection([ee.Feature(roi_geom, {'name': 'roi'})])
    )
    
    image_collection_filt = (image_collection.filter(filt_time).filter(filt_roi))
    
    image_collection_ndvi = image_collection_filt.map(ndvi)
    
    image_collection_ndvi = image_collection_ndvi.getRegion(
        roi_geom.centroid(), 
        scale=250).getInfo()
    
    image_collection_df = pd.DataFrame(image_collection_ndvi[1:], columns=image_collection_ndvi[0])
    image_collection_df.sort_values('time', inplace=True)
    
    return image_collection_df


def ndvi(image):
    value = image.normalizedDifference(
        ['sur_refl_b02', 'sur_refl_b01']).rename('ndvi')
    result = image.addBands(value).select('ndvi')
    return result
