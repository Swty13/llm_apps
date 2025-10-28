#!/usr/bin/env python3
import streamlit as st
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time
from reddit_sync_client import get_reddit_client

# Page configuration
st.set_page_config(
    page_title="Reddit MCP Explorer",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        background: linear-gradient(90deg, #ff6b6b, #ee5a24);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 1rem;
    }

    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }

    .post-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #ff6b6b;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    .success-box {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }

    .error-box {
        background: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }

    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'reddit_client' not in st.session_state:
    st.session_state.reddit_client = None
if 'client_initialized' not in st.session_state:
    st.session_state.client_initialized = False

def initialize_client():
    """Initialize Reddit client"""
    if not st.session_state.client_initialized:
        try:
            st.session_state.reddit_client = get_reddit_client()
            st.session_state.client_initialized = True
            return True
        except Exception as e:
            st.error(f"Failed to initialize client: {e}")
            return False
    return True

# Main header
st.markdown('<h1 class="main-header">🔥 Reddit MCP Explorer</h1>', unsafe_allow_html=True)
st.markdown("### Beautiful interface for exploring Reddit with MCP")

# Sidebar
with st.sidebar:
    st.markdown("## 🎛️ Control Panel")

    # Initialize client button
    if not st.session_state.client_initialized:
        if st.button("🚀 Initialize Reddit Client", type="primary"):
            with st.spinner("Connecting to Reddit MCP server..."):
                if initialize_client():
                    st.success("✅ Connected successfully!")
                    st.rerun()
    else:
        st.success("✅ Reddit Client Connected")

    st.markdown("---")

    # Tool selection
    tool = st.selectbox(
        "🔧 Select Tool",
        ["Hot Posts", "Search Posts", "Get Comments", "Subreddit Info", "Create Post", "Analytics Dashboard"]
    )

# Main content area
if not st.session_state.client_initialized:
    st.info("👆 Please initialize the Reddit client using the sidebar first!")
    st.stop()

if tool == "Hot Posts":
    st.markdown("## 🔥 Hot Posts Explorer")

    col1, col2 = st.columns([3, 1])
    with col1:
        subreddit = st.text_input("📋 Subreddit", value="python", placeholder="Enter subreddit name")
    with col2:
        limit = st.number_input("📊 Number of posts", min_value=1, max_value=50, value=10)

    if st.button("🔍 Fetch Posts", type="primary"):
        if subreddit:
            # Clean up subreddit name
            clean_subreddit = subreddit.strip().replace("r/", "").replace(" ", "")
            if not clean_subreddit:
                st.error("Please enter a valid subreddit name!")
            else:
                with st.spinner(f"Fetching posts from r/{clean_subreddit}..."):
                    try:
                        result = st.session_state.reddit_client.fetch_posts(clean_subreddit, limit)

                        if result and 'posts' in result:
                            posts = result['posts']

                            # Display metrics
                            col1, col2, col3, col4 = st.columns(4)
                            with col1:
                                avg_score = sum(post['score'] for post in posts) / len(posts)
                                st.metric("📈 Avg Score", f"{avg_score:.1f}")
                            with col2:
                                total_comments = sum(post['num_comments'] for post in posts)
                                st.metric("💬 Total Comments", f"{total_comments:,}")
                            with col3:
                                avg_ratio = sum(post['upvote_ratio'] for post in posts) / len(posts)
                                st.metric("👍 Avg Upvote %", f"{avg_ratio*100:.1f}%")
                            with col4:
                                st.metric("📋 Posts Found", len(posts))

                            # Display posts
                            st.markdown("### 📰 Posts")
                            for i, post in enumerate(posts, 1):
                                with st.expander(f"{i}. {post['title'][:80]}..." if len(post['title']) > 80 else f"{i}. {post['title']}", expanded=False):
                                    col1, col2 = st.columns([3, 1])
                                    with col1:
                                        st.markdown(f"**👤 Author:** u/{post['author']}")
                                        st.markdown(f"**🔗 Link:** [View on Reddit]({post['permalink']})")
                                        if post['selftext']:
                                            st.markdown(f"**📝 Content:** {post['selftext'][:200]}...")
                                    with col2:
                                        st.metric("⬆️ Score", post['score'])
                                        st.metric("💬 Comments", post['num_comments'])
                                        st.metric("📊 Upvote %", f"{post['upvote_ratio']*100:.1f}%")

                                    # Quick action buttons
                                    col1, col2 = st.columns(2)
                                    with col1:
                                        if st.button(f"💬 View Comments", key=f"comments_{i}"):
                                            st.session_state.comment_post_id = post['id']
                                            st.rerun()
                                    with col2:
                                        if st.button(f"📊 Analyze", key=f"analyze_{i}"):
                                            st.session_state.analyze_post = post
                                            st.rerun()
                        else:
                            st.warning("No posts found!")

                    except Exception as e:
                        st.error(f"❌ Error: {e}")
        else:
            st.warning("Please enter a subreddit name!")

elif tool == "Search Posts":
    st.markdown("## 🔍 Search Posts")

    col1, col2 = st.columns([2, 1])
    with col1:
        search_subreddit = st.text_input("📋 Subreddit", value="technology", placeholder="Enter subreddit name")
        search_query = st.text_input("🔍 Search Query", placeholder="artificial intelligence")
    with col2:
        search_limit = st.number_input("📊 Results", min_value=1, max_value=50, value=10)

    if st.button("🔎 Search", type="primary"):
        if search_subreddit and search_query:
            with st.spinner(f"Searching r/{search_subreddit} for '{search_query}'..."):
                try:
                    result = st.session_state.reddit_client.search_posts(search_subreddit, search_query, search_limit)

                    if result and 'posts' in result:
                        posts = result['posts']

                        if posts:
                            st.success(f"✅ Found {len(posts)} posts matching '{search_query}'")

                            # Results visualization
                            if len(posts) > 1:
                                scores = [post['score'] for post in posts]
                                titles = [post['title'][:30] + "..." for post in posts]

                                fig = px.bar(
                                    x=titles,
                                    y=scores,
                                    title="Search Results by Score",
                                    labels={'x': 'Posts', 'y': 'Score'}
                                )
                                fig.update_layout(xaxis_tickangle=-45)
                                st.plotly_chart(fig, use_container_width=True)

                            # Display results
                            for i, post in enumerate(posts, 1):
                                with st.container():
                                    col1, col2 = st.columns([4, 1])
                                    with col1:
                                        st.markdown(f"**{i}. {post['title']}**")
                                        st.markdown(f"👤 u/{post['author']} • 📅 {datetime.fromtimestamp(post['created_utc']).strftime('%Y-%m-%d')}")
                                        if post['selftext']:
                                            st.markdown(f"_{post['selftext'][:150]}..._")
                                    with col2:
                                        st.metric("⬆️", post['score'])
                                        st.metric("💬", post['num_comments'])

                                    st.markdown(f"[🔗 View Post]({post['permalink']})")
                                    st.markdown("---")
                        else:
                            st.warning("No posts found for this search!")

                except Exception as e:
                    st.error(f"❌ Error: {e}")
        else:
            st.warning("Please enter both subreddit and search query!")

elif tool == "Get Comments":
    st.markdown("## 💬 Get Comments")

    # Check if we have a post ID from the Hot Posts section
    if 'comment_post_id' in st.session_state:
        default_post_id = st.session_state.comment_post_id
        del st.session_state.comment_post_id
    else:
        default_post_id = ""

    post_id = st.text_input("📝 Post ID", value=default_post_id, placeholder="Enter Reddit post ID (without t3_ prefix)")

    if st.button("📥 Get Comments", type="primary"):
        if post_id:
            with st.spinner("Fetching comments..."):
                try:
                    result = st.session_state.reddit_client.get_comments(post_id)

                    if result and 'comments' in result:
                        post_info = result['post']
                        comments = result['comments']

                        # Post information
                        st.markdown("### 📰 Post Information")
                        with st.container():
                            st.markdown(f"**{post_info['title']}**")
                            st.markdown(f"👤 u/{post_info['author']} • ⬆️ {post_info['score']} points")
                            st.markdown(f"[🔗 View on Reddit]({post_info['permalink']})")

                        # Comments analysis
                        if comments:
                            st.markdown(f"### 💬 Comments ({len(comments)})")

                            # Comment statistics
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                avg_score = sum(c['score'] for c in comments) / len(comments)
                                st.metric("📈 Avg Score", f"{avg_score:.1f}")
                            with col2:
                                top_score = max(c['score'] for c in comments)
                                st.metric("🏆 Top Score", top_score)
                            with col3:
                                st.metric("📝 Total Comments", len(comments))

                            # Sort options
                            sort_by = st.selectbox("📊 Sort by", ["Score (High to Low)", "Score (Low to High)", "Newest", "Oldest"])

                            if sort_by == "Score (High to Low)":
                                comments = sorted(comments, key=lambda x: x['score'], reverse=True)
                            elif sort_by == "Score (Low to High)":
                                comments = sorted(comments, key=lambda x: x['score'])
                            elif sort_by == "Newest":
                                comments = sorted(comments, key=lambda x: x['created_utc'], reverse=True)
                            else:  # Oldest
                                comments = sorted(comments, key=lambda x: x['created_utc'])

                            # Display comments
                            max_comments = st.slider("Max comments to show", 5, min(50, len(comments)), 20)

                            for i, comment in enumerate(comments[:max_comments], 1):
                                with st.expander(f"Comment {i} • ⬆️ {comment['score']} • u/{comment['author']}", expanded=False):
                                    st.markdown(comment['body'])
                                    st.caption(f"Posted: {datetime.fromtimestamp(comment['created_utc']).strftime('%Y-%m-%d %H:%M')}")
                        else:
                            st.info("No comments found for this post.")

                except Exception as e:
                    st.error(f"❌ Error: {e}")
        else:
            st.warning("Please enter a post ID!")

elif tool == "Subreddit Info":
    st.markdown("## ℹ️ Subreddit Information")

    info_subreddit = st.text_input("📋 Subreddit", value="datascience", placeholder="Enter subreddit name")

    if st.button("📊 Get Info", type="primary"):
        if info_subreddit:
            # Clean up subreddit name
            clean_subreddit = info_subreddit.strip().replace("r/", "").replace(" ", "")
            if not clean_subreddit:
                st.error("Please enter a valid subreddit name!")
            else:
                with st.spinner(f"Fetching info for r/{clean_subreddit}..."):
                    try:
                        result = st.session_state.reddit_client.get_subreddit_info(clean_subreddit)

                        if result:
                            # Header
                            st.markdown(f"### r/{result['name']}")
                            st.markdown(f"**{result['title']}**")

                            # Key metrics
                            col1, col2, col3, col4 = st.columns(4)
                            with col1:
                                st.metric("👥 Subscribers", f"{result['subscribers']:,}")
                            with col2:
                                active = result.get('active_users', 'N/A')
                                st.metric("🟢 Active Users", active if active != 'N/A' else 'N/A')
                            with col3:
                                created_year = datetime.fromtimestamp(result['created_utc']).year
                                st.metric("📅 Created", created_year)
                            with col4:
                                nsfw = "Yes" if result.get('over18') else "No"
                                st.metric("🔞 NSFW", nsfw)

                            # Description
                            st.markdown("### 📝 Description")
                            st.markdown(result['public_description'])

                            if result.get('description'):
                                with st.expander("📖 Full Description"):
                                    st.markdown(result['description'])

                            # Rules
                            if result.get('rules'):
                                st.markdown("### 📋 Rules")
                                for i, rule in enumerate(result['rules'], 1):
                                    with st.expander(f"Rule {i}: {rule['short_name']}"):
                                        st.markdown(rule.get('description', 'No description available'))

                            # Quick actions
                            st.markdown("### 🚀 Quick Actions")
                            col1, col2 = st.columns(2)
                            with col1:
                                if st.button("🔥 View Hot Posts"):
                                    st.session_state.hot_posts_subreddit = clean_subreddit
                                    st.rerun()
                            with col2:
                                st.markdown(f"[🔗 Visit r/{result['name']}]({result['url']})")

                    except Exception as e:
                        st.error(f"❌ Error: {e}")
        else:
            st.warning("Please enter a subreddit name!")

elif tool == "Create Post":
    st.markdown("## ➕ Create New Post")

    st.warning("⚠️ Make sure your Reddit app is configured as 'script' type for posting!")

    with st.form("create_post_form"):
        post_subreddit = st.text_input("📋 Subreddit", placeholder="test")
        post_title = st.text_input("📝 Title", placeholder="Your awesome post title")

        post_type = st.radio("📄 Post Type", ["Text Post", "Link Post"])

        if post_type == "Text Post":
            post_content = st.text_area("✍️ Content", placeholder="Write your post content here...")
            post_url = None
        else:
            post_content = None
            post_url = st.text_input("🔗 URL", placeholder="https://example.com")

        submitted = st.form_submit_button("🚀 Create Post", type="primary")

        if submitted:
            if post_subreddit and post_title:
                if post_type == "Text Post" and not post_content:
                    st.error("Please enter post content for text posts!")
                elif post_type == "Link Post" and not post_url:
                    st.error("Please enter URL for link posts!")
                else:
                    with st.spinner("Creating post..."):
                        try:
                            result = st.session_state.reddit_client.post_to_subreddit(
                                post_subreddit, post_title, post_content, post_url
                            )

                            if result.get('success'):
                                st.success("✅ Post created successfully!")
                                st.markdown(f"[🔗 View your post]({result['post_url']})")
                                st.balloons()
                            else:
                                st.error(f"❌ Failed to create post: {result}")

                        except Exception as e:
                            st.error(f"❌ Error: {e}")
            else:
                st.warning("Please fill in all required fields!")

elif tool == "Analytics Dashboard":
    st.markdown("## 📊 Analytics Dashboard")

    st.info("🚀 Fetch some posts first to see analytics!")

    col1, col2 = st.columns(2)
    with col1:
        analysis_subreddit = st.text_input("📋 Subreddit for Analysis", value="programming")
    with col2:
        analysis_limit = st.number_input("📊 Posts to Analyze", min_value=10, max_value=100, value=25)

    if st.button("🔍 Generate Analytics", type="primary"):
        if analysis_subreddit:
            with st.spinner("Generating analytics..."):
                try:
                    result = st.session_state.reddit_client.fetch_posts(analysis_subreddit, analysis_limit)

                    if result and 'posts' in result:
                        posts = result['posts']

                        # Create DataFrame for analysis
                        df = pd.DataFrame(posts)

                        # Metrics overview
                        st.markdown("### 📈 Overview Metrics")
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("Total Posts", len(posts))
                        with col2:
                            avg_score = df['score'].mean()
                            st.metric("Avg Score", f"{avg_score:.1f}")
                        with col3:
                            total_comments = df['num_comments'].sum()
                            st.metric("Total Comments", f"{total_comments:,}")
                        with col4:
                            avg_ratio = df['upvote_ratio'].mean()
                            st.metric("Avg Upvote %", f"{avg_ratio*100:.1f}%")

                        # Visualizations
                        col1, col2 = st.columns(2)

                        with col1:
                            # Score distribution
                            fig_score = px.histogram(
                                df, x='score', nbins=20,
                                title="Score Distribution",
                                labels={'score': 'Post Score', 'count': 'Number of Posts'}
                            )
                            st.plotly_chart(fig_score, use_container_width=True)

                            # Top authors
                            author_counts = df['author'].value_counts().head(10)
                            fig_authors = px.bar(
                                x=author_counts.values,
                                y=author_counts.index,
                                orientation='h',
                                title="Top 10 Most Active Authors",
                                labels={'x': 'Number of Posts', 'y': 'Author'}
                            )
                            st.plotly_chart(fig_authors, use_container_width=True)

                        with col2:
                            # Comments vs Score scatter
                            fig_scatter = px.scatter(
                                df, x='score', y='num_comments',
                                title="Comments vs Score Correlation",
                                labels={'score': 'Post Score', 'num_comments': 'Number of Comments'},
                                hover_data=['title']
                            )
                            st.plotly_chart(fig_scatter, use_container_width=True)

                            # Upvote ratio distribution
                            fig_ratio = px.box(
                                df, y='upvote_ratio',
                                title="Upvote Ratio Distribution",
                                labels={'upvote_ratio': 'Upvote Ratio'}
                            )
                            st.plotly_chart(fig_ratio, use_container_width=True)

                        # Top performing posts
                        st.markdown("### 🏆 Top Performing Posts")
                        top_posts = df.nlargest(5, 'score')[['title', 'author', 'score', 'num_comments', 'upvote_ratio']]
                        st.dataframe(top_posts, use_container_width=True)

                        # Time analysis (if we have timestamp data)
                        if 'created_utc' in df.columns:
                            df['created_datetime'] = pd.to_datetime(df['created_utc'], unit='s')
                            df['hour'] = df['created_datetime'].dt.hour

                            hourly_avg = df.groupby('hour')['score'].mean().reset_index()
                            fig_time = px.line(
                                hourly_avg, x='hour', y='score',
                                title="Average Post Score by Hour of Day",
                                labels={'hour': 'Hour of Day', 'score': 'Average Score'}
                            )
                            st.plotly_chart(fig_time, use_container_width=True)

                except Exception as e:
                    st.error(f"❌ Error: {e}")
        else:
            st.warning("Please enter a subreddit name!")

# Footer
st.markdown("---")
st.markdown("### 🛠️ Built with Streamlit & Reddit MCP")
st.markdown("💡 **Tip:** Use the sidebar to navigate between different tools and features!")