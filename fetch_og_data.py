import xarray as xr
import os

print("🚀 Fetching OG Scientific NetCDF data (NCEP/NCAR Reanalysis)...")

# Ye function seedha NOAA/UCAR ke servers se 15MB ka asli data uthata hai
try:
    ds = xr.tutorial.load_dataset("air_temperature")
    
    # Save it locally so we don't need internet during the pitch
    file_name = "og_climate_data.nc"
    ds.to_netcdf(file_name)
    
    print(f"✅ SUCCESS! '{file_name}' is now in your folder.")
    print(f"📊 Variables found: {list(ds.data_vars)} (Variable name is 'air')")
    print(f"🌍 Coverage: {ds.lat.size} latitudes x {ds.lon.size} longitudes")
except Exception as e:
    print(f"❌ Error fetching data: {e}")
