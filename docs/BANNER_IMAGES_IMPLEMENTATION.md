# Banner Images Implementation

This document describes the implementation of banner images for blue posts and news articles in the Azeroth Herald Discord bot.

## Overview

The bot now includes banner images in Discord embeds for both blue tracker posts and Wowhead news articles, providing a more visually engaging experience for users.

## Implementation Details

### Data Structure Changes

#### Blue Tracker Posts
- Added `image_url` field to post data structure
- Extracts images from JSON data fields: `image`, `banner`, `thumbnail`, `img`
- Parses HTML content for `<img>` tags when direct image fields are unavailable
- Validates image URLs to ensure they're appropriate post images

#### Wowhead News Articles
- Added `image_url` field to article data structure
- Includes placeholder thematic images for sample articles
- HTML parsing functionality to extract article banners from real content
- Image validation to filter out non-article images (icons, avatars, ads)

### Image Extraction Logic

#### Wowhead News Scraper (`src/utils/wowhead_news.py`)
```python
# Real HTML structure parsing for Wowhead news cards
news_cards = soup.find_all('a', class_='news-card-simple-thumbnail')

for card in news_cards:
    # Extract article URL from href
    article_url = card.get('href', '')
    
    # Extract banner image from img tag
    img_tag = card.find('img')
    if img_tag:
        image_url = img_tag.get('src', '')
        title = img_tag.get('alt', '')

# Expected HTML structure:
# <a href="/news/article-url" class="news-card-simple-thumbnail">
#   <img src="https://wow.zamimg.com/uploads/blog/images/50237-article-name.jpg" 
#        alt="Article Title" loading="lazy">
# </a>
```

#### Blue Tracker Scraper (`src/utils/blue_tracker.py`)
```python
# Direct image field extraction
image_url = entry.get('image') or entry.get('banner') or entry.get('thumbnail')

# Content parsing for embedded images
if not image_url and body:
    image_url = self._extract_image_from_content(body)

# URL normalization
if image_url.startswith('/'):
    image_url = f"https://www.wowhead.com{image_url}"
```

### Embed Enhancement

#### Discord Embed Updates (`src/utils/embeds.py`)
```python
# Image display logic
if image_url:
    embed.set_image(url=image_url)  # Large banner image
    embed.set_thumbnail(url=fallback_thumbnail)  # Consistent branding
else:
    thematic_image = _get_thematic_image_for_post(post_data)
    if thematic_image:
        embed.set_image(url=thematic_image)
    embed.set_thumbnail(url=fallback_thumbnail)
```

### Thematic Image System

When original images aren't available, the bot selects appropriate WoW-themed images based on content analysis:

#### Content Categories and Images

| Content Type | Keywords | Image |
|--------------|----------|-------|
| Mythic+ | mythic, dungeon, m+, keystone, affix | Mythic dungeon achievement |
| Raids | raid, boss, encounter, tier | Raid achievement image |
| PvP | pvp, arena, battleground, honor | PvP achievement image |
| Classes | class, spec, tuning, balance | Character achievement |
| Technical | hotfix, maintenance, server | Engineering/technical icon |
| Events | season, event, holiday | Seasonal achievement |
| General | patch, update, news | General WoW achievement |

#### Implementation
```python
def _get_thematic_image_for_post(post_data):
    title = post_data.get('title', '').lower()
    content = post_data.get('content_preview', '').lower()
    combined_text = f"{title} {content}"
    
    # Keyword matching against image mappings
    for keywords, image_url in image_mappings.items():
        if any(keyword in combined_text for keyword in keywords):
            return image_url
    
    return None
```

## Visual Experience

### Banner Display
- **Primary Images**: Original post/article banners when available
- **Fallback Images**: Thematic WoW images based on content analysis
- **Thumbnails**: Consistent branding (Blizzard logo for posts, Wowhead icon for articles)

### Image Sources
- **Blizzard Official**: `blizzard.com`, `battle.net`
- **Wowhead News**: `wow.zamimg.com/uploads/blog/images/` (primary article banners)
- **Wowhead Icons**: `wow.zamimg.com/images/wow/icons/` (achievement and game assets)
- **WoW General**: Achievement and game asset images for thematic fallbacks

### Quality Assurance
- **URL Validation**: Ensures images are from trusted sources
- **Size Filtering**: Excludes small icons and navigation elements
- **Content Relevance**: Matches images to post/article topics
- **Fallback System**: Always provides appropriate imagery

## Benefits

### User Experience
- **Visual Appeal**: Rich, engaging Discord embeds
- **Content Recognition**: Quick visual identification of post types
- **Consistent Branding**: Maintains bot identity across all posts
- **Information Hierarchy**: Images complement rather than distract from text

### Technical Benefits
- **Graceful Degradation**: Functions properly even when images fail to load
- **Performance**: Minimal impact on load times
- **Scalability**: Easy to add new image categories and sources
- **Maintainability**: Clean separation of image logic from core functionality

## Configuration

### Image URL Sources
The system handles various URL formats:
- Absolute URLs: `https://example.com/image.jpg`
- Protocol-relative: `//example.com/image.jpg`
- Site-relative: `/images/example.jpg`
- Resource paths: `images/example.jpg`

### Validation Patterns
```python
# Wowhead-specific validation
if 'wow.zamimg.com/uploads/blog/images' in src_lower:
    return True  # Primary Wowhead article images

# Trusted domains for image sources
trusted_domains = ['blizzard.com', 'battle.net', 'wowhead.com', 'wow.zamimg.com']

# Content indicators for valid images
good_patterns = ['news', 'article', 'post', 'content', 'hero', 'banner', 'uploads']

# Patterns to avoid
skip_patterns = ['tiny', 'small', 'favicon', 'icon-', 'avatar', 'button', 'nav']
```

### Real-World HTML Structure

Based on actual Wowhead news pages, banner images follow this structure:
```html
<a href="/news/article-slug-id" class="news-card-simple-thumbnail">
    <img src="https://wow.zamimg.com/uploads/blog/images/ID-article-name.jpg" 
         alt="Article Title" 
         loading="lazy">
</a>
```

The scraper specifically looks for:
- `<a>` tags with class `news-card-simple-thumbnail`
- `<img>` tags within those links
- `src` attributes containing the banner URL
- `alt` attributes for the article title

## Future Enhancements

### Potential Improvements
- **Image Caching**: Store processed images locally to reduce external requests
- **Dynamic Resizing**: Optimize image dimensions for Discord display
- **Additional Sources**: Expand to include more WoW community sites
- **AI Enhancement**: Use content analysis for better image selection
- **User Preferences**: Allow servers to customize image themes

### Monitoring
- **Error Handling**: Robust fallbacks for failed image loads
- **Performance Metrics**: Track image load success rates
- **User Feedback**: Monitor effectiveness of thematic image selection

## Testing

### Test Commands
```bash
# Test blue tracker with image display
!bluetrack test

# Test news articles with images  
!news latest

# View sample posts with different content types
!bluetrack latest  # Shows various post types
!news reset       # Shows reset-relevant articles
```

### Validation
- Test image extraction from various post formats
- Verify thematic image selection for different content types
- Ensure graceful handling of missing or invalid images
- Confirm consistent thumbnail display across all embeds

This implementation significantly enhances the visual appeal of the bot while maintaining reliability and performance.
