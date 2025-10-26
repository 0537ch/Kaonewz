from fastapi import FastAPI, HTTPException, status, Query, Path
from fastapi.middleware.cors import CORSMiddleware
import requests
import pandas as pd
from typing import List, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import services
from services.news_service import news_service

app = FastAPI(
    title="Country Analytics API",
    description="API for country data analysis with news integration",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_country_data():
    url = "https://restcountries.com/v3.1/all?fields=name,region,population,area"
    resp = requests.get(url)
    data = resp.json()
    df = pd.json_normalize(data)
    df = df[['name.common', 'region', 'population', 'area']]
    df.columns = ['country', 'region', 'population', 'area_km2']
    df['density'] = df['population'] / df['area_km2']
    return df


# Root endpoint
@app.get("/", tags=["Root"])
async def home():
    return {
        "message": "Country Analytics API is running 🚀",
        "endpoints": {
            "countries": "/countries",
            "country_news": "/news/country/{country_code}",
            "search_news": "/news/search"
        }
    }


# All countries
@app.get("/countries", tags=["Countries"])
async def all_countries():
    """
    Get data for all countries including basic information.
    """
    try:
        df = get_country_data()
        return {
            "status": "success",
            "results": len(df),
            "data": df.to_dict(orient="records")
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching country data: {str(e)}"
        )


# Region Filter
@app.get("/countries/region/{region}", tags=["Countries"])
async def countries_by_region(region: str):
    """
    Get countries by region.
    """
    try:
        df = get_country_data()
        df_region = df[df["region"].str.lower() == region.lower()]
        
        if df_region.empty:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No countries found in region: {region}"
            )
            
        return {
            "status": "success",
            "region": region,
            "results": len(df_region),
            "data": df_region.to_dict(orient="records")
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing request: {str(e)}"
        )


# Population
@app.get("/countries/top/{n}", tags=["Countries"])
async def top_countries_by_population(
    n: int = Path(..., gt=0, le=50, description="Number of top countries to return (max 50)")
):
    """
    Get top N most populous countries.
    """
    try:
        df = get_country_data()
        df_sorted = df.sort_values("population", ascending=False).head(n)
        
        return {
            "status": "success",
            "results": len(df_sorted),
            "data": df_sorted.to_dict(orient="records")
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing request: {str(e)}"
        )

# Average Statistic
@app.get("/stats/region", tags=["Statistics"])
async def region_stats():
    """
    Get average statistics by region.
    """
    try:
        df = get_country_data()
        grouped = (
            df.groupby("region")[["population", "density", "area_km2"]]
            .mean()
            .reset_index()
        )
        grouped = grouped.round(2)
        
        return {
            "status": "success",
            "results": len(grouped),
            "data": grouped.to_dict(orient="records")
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing request: {str(e)}"
        )

# Top Density
@app.get("/countries/density/top/{n}", tags=["Countries"])
async def top_density(
    n: int = Path(..., gt=0, le=50, description="Number of top countries to return (max 50)")
):
    """
    Get top N most densely populated countries.
    """
    try:
        df = get_country_data()
        top_density = df.sort_values("density", ascending=False).head(n)
        
        return {
            "status": "success",
            "results": len(top_density),
            "data": top_density.to_dict(orient="records")
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing request: {str(e)}"
        )

# News Endpoints
@app.get("/news/country/{country_code}", tags=["News"])
async def get_country_news(
    country_code: str,
    page_size: int = Query(10, gt=0, le=100, description="Number of results per page (max 100)"),
    page: int = Query(1, ge=1, description="Page number"),
    category: Optional[str] = Query(None, description="News category (business, entertainment, general, health, science, sports, technology)")
):
    """
    Get top news headlines for a specific country.
    """
    try:
        articles = news_service.get_news_for_country(
            country_code=country_code,
            page_size=page_size,
            page=page,
            category=category
        )
        
        return {
            "status": "success",
            "country": country_code.upper(),
            "category": category,
            "page": page,
            "page_size": page_size,
            "results": len(articles),
            "data": articles
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching news: {str(e)}"
        )

@app.get("/news/search", tags=["News"])
async def search_news(
    query: str = Query(..., min_length=2, description="Search query"),
    country_code: Optional[str] = Query(None, min_length=2, max_length=2, description="2-letter country code"),
    language: str = Query("en", description="Language code (e.g., en, es, fr)"),
    sort_by: str = Query("publishedAt", description="Sort by: publishedAt, popularity, or relevancy"),
    page_size: int = Query(10, gt=0, le=100, description="Number of results per page (max 100)"),
    page: int = Query(1, ge=1, description="Page number")
):
    """
    Search for news articles.
    """
    try:
        articles = news_service.search_news(
            query=query,
            country_code=country_code,
            language=language,
            sort_by=sort_by,
            page_size=page_size,
            page=page
        )
        
        return {
            "status": "success",
            "query": query,
            "country": country_code.upper() if country_code else None,
            "language": language,
            "sort_by": sort_by,
            "page": page,
            "page_size": page_size,
            "results": len(articles),
            "data": articles
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error searching news: {str(e)}"
        )
