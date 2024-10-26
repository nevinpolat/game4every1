# analytics.py

import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy.orm import Session
from models import User, Feedback, SearchedGame, ChatHistory
from sqlalchemy import func

def show_analytics(session: Session):
    """
    Displays comprehensive analytics dashboards for users, feedback, games, chat history, and search performance.

    Args:
        session (Session): SQLAlchemy session connected to the PostgreSQL database.
    """
    st.title("📈 Comprehensive Analytics Dashboard")
    
    # Create tabs for different analytics sections
    tabs = st.tabs([
        "User Analytics", 
        "Feedback Analytics", 
        "Game Analytics", 
        "Chat History Analytics", 
        "Search Performance Metrics"
    ])
    
    with tabs[0]:
        user_analytics(session)
    
    with tabs[1]:
        feedback_analytics(session)
    
    with tabs[2]:
        game_analytics(session)
    
    with tabs[3]:
        chat_history_analytics(session)
    
    with tabs[4]:
        search_performance_metrics(session)

def user_analytics(session: Session):
    """
    Displays user-related analytics including total users, gender distribution, age distribution,
    and new user registrations over time.

    Args:
        session (Session): SQLAlchemy session.
    """
    st.header("👤 User Analytics")
    
    # Total Users
    total_users = session.query(func.count(User.user_id)).scalar()
    st.metric("Total Users", int(total_users))
    
    # Users by Gender
    st.markdown("### Users by Gender")
    gender_data = session.query(User.gender, func.count(User.user_id)).group_by(User.gender).all()
    gender_df = pd.DataFrame(gender_data, columns=["Gender", "Count"])
    
    if not gender_df.empty:
        fig_gender = px.pie(
            gender_df, 
            names='Gender', 
            values='Count',
            color='Gender',
            color_discrete_sequence=px.colors.sequential.Reds
        )
        fig_gender.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_gender, use_container_width=True)
    else:
        st.info("No gender data available.")
    
    # Users by Age Distribution
    st.markdown("### Age Distribution of Users")
    age_data = session.query(User.age).all()
    age_df = pd.DataFrame(age_data, columns=["Age"])
    
    if not age_df.empty:
        fig_age = px.histogram(
            age_df, 
            x='Age', 
            nbins=20,
            labels={'Age': 'Age'},
            color_discrete_sequence=px.colors.sequential.Reds
        )
        fig_age.update_traces(opacity=0.95)
        fig_age.update_layout(
            xaxis_title="Age",
            yaxis_title="Number of Users",
            bargap=0.1
        )
        st.plotly_chart(fig_age, use_container_width=True)
    else:
        st.info("No age data available.")
    
    # New Users Over Time
    st.markdown("### New User Registrations Over Time")
    new_users = session.query(
        func.date_trunc('month', User.registration_time).label('month'),
        func.count(User.user_id)
    ).group_by('month').order_by('month').all()
    new_users_df = pd.DataFrame(new_users, columns=["Month", "New Users"])
    new_users_df['Month'] = pd.to_datetime(new_users_df['Month'])
    
    if not new_users_df.empty and new_users_df['New Users'].sum() > 0:
        fig_new_users = px.line(
            new_users_df, 
            x='Month', 
            y='New Users',
            markers=True,
            labels={'Month': 'Month', 'New Users': 'Number of New Users'},
            color_discrete_sequence=px.colors.sequential.Reds
        )
        fig_new_users.update_layout(
            xaxis=dict(
                tickformat="%b %Y",
                tickangle=-45
            ),
            yaxis=dict(tickprefix=""),
        )
        st.plotly_chart(fig_new_users, use_container_width=True)
    else:
        st.info("No new user registrations to display.")

def feedback_analytics(session: Session):
    """
    Displays feedback-related analytics including total feedbacks, feedback type distribution,
    feedbacks over time, and feedback per user.

    Args:
        session (Session): SQLAlchemy session.
    """
    st.header("📝 Feedback Analytics")
    
    # Total Feedbacks
    total_feedbacks = session.query(func.count(Feedback.feedback_id)).scalar()
    st.metric("Total Feedbacks", int(total_feedbacks))
    
    # Feedback Types Distribution
    st.markdown("### Feedback Types Distribution")
    feedback_types = session.query(
        Feedback.feedback_type, 
        func.count(Feedback.feedback_id)
    ).group_by(Feedback.feedback_type).all()
    feedback_types_df = pd.DataFrame(feedback_types, columns=["Feedback Type", "Count"])
    
    if not feedback_types_df.empty:
        fig_feedback_types = px.pie(
            feedback_types_df, 
            names='Feedback Type', 
            values='Count',
            hole=0.4,
            color='Feedback Type',
            color_discrete_sequence=px.colors.sequential.Blues
        )
        fig_feedback_types.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_feedback_types, use_container_width=True)
    else:
        st.info("No feedback type data available.")
    
    # Feedbacks Over Time
    st.markdown("### Feedbacks Over Time")
    feedback_over_time = session.query(
        func.date_trunc('month', Feedback.feedback_time).label('month'),
        func.count(Feedback.feedback_id)
    ).group_by('month').order_by('month').all()
    feedback_over_time_df = pd.DataFrame(feedback_over_time, columns=["Month", "Feedback Count"])
    feedback_over_time_df['Month'] = pd.to_datetime(feedback_over_time_df['Month'])
    
    if not feedback_over_time_df.empty and feedback_over_time_df['Feedback Count'].sum() > 0:
        fig_feedback_time = px.line(
            feedback_over_time_df, 
            x='Month', 
            y='Feedback Count',
            markers=True,
            labels={'Month': 'Month', 'Feedback Count': 'Number of Feedbacks'},
            color_discrete_sequence=px.colors.sequential.Oranges
        )
        fig_feedback_time.update_layout(
            xaxis=dict(
                tickformat="%b %Y",
                tickangle=-45
            ),
            yaxis=dict(tickprefix=""),
        )
        st.plotly_chart(fig_feedback_time, use_container_width=True)
    else:
        st.info("No feedback data available.")
    
    # Feedback per User (Only Upvotes)
    st.markdown("### Top 10 Users by Upvote Feedback Count")
    feedback_per_user = session.query(
        User.user_name, 
        func.count(Feedback.feedback_id).label('Feedback Count')
    ).join(Feedback, User.user_id == Feedback.user_id)\
     .filter(Feedback.feedback_type == 'up')\
     .group_by(User.user_name)\
     .order_by(func.count(Feedback.feedback_id).desc())\
     .limit(10)\
     .all()
    
    feedback_per_user_df = pd.DataFrame(feedback_per_user, columns=["User Name", "Feedback Count"])
    
    if not feedback_per_user_df.empty:
        fig_feedback_user = px.bar(
            feedback_per_user_df, 
            x='Feedback Count', 
            y='User Name',
            orientation='h',
            text='Feedback Count',
            color='Feedback Count',
            color_continuous_scale=px.colors.sequential.Viridis
        )
        fig_feedback_user.update_traces(texttemplate='%{text}', textposition='outside')
        fig_feedback_user.update_layout(
            xaxis=dict(title='Number of Upvotes'),
            yaxis=dict(title='User Name'),
            showlegend=False,
        )
        st.plotly_chart(fig_feedback_user, use_container_width=True)
    else:
        st.info("No upvote feedback available.")

def game_analytics(session: Session):
    """
    Displays game-related analytics including total searched games, top searched games,
    searched games by category and subcategory, and game searches over time.

    Args:
        session (Session): SQLAlchemy session.
    """
    st.header("🎮 Game Analytics")
    
    # Total Searched Games
    total_searched_games = session.query(func.count(SearchedGame.game_id)).scalar()
    st.metric("Total Searched Games", int(total_searched_games))
    
    # Top Searched Games
    st.markdown("### Top 10 Searched Games")
    top_games = session.query(
        SearchedGame.game_name, 
        func.count(SearchedGame.game_id).label('Search Count')
    ).group_by(SearchedGame.game_name)\
     .order_by(func.count(SearchedGame.game_id).desc())\
     .limit(10)\
     .all()
    top_games_df = pd.DataFrame(top_games, columns=["Game Name", "Search Count"])
    
    if not top_games_df.empty:
        fig_top_games = px.bar(
            top_games_df, 
            x='Search Count', 
            y='Game Name',
            orientation='h',
            text='Search Count',
            color='Search Count',
            color_continuous_scale=px.colors.sequential.Viridis
        )
        fig_top_games.update_traces(texttemplate='%{text}', textposition='outside')
        fig_top_games.update_layout(
            xaxis=dict(title='Number of Searches'),
            yaxis=dict(title='Game Name'),
            showlegend=False,
        )
        st.plotly_chart(fig_top_games, use_container_width=True)
    else:
        st.info("No game search data available.")
    
    # Searched Games by Category
    st.markdown("### Searched Games by Category")
    games_by_category = session.query(
        SearchedGame.category, 
        func.count(SearchedGame.game_id)
    ).group_by(SearchedGame.category).all()
    games_by_category_df = pd.DataFrame(games_by_category, columns=["Category", "Count"])
    
    if not games_by_category_df.empty:
        # Pie Chart
        fig_category_pie = px.pie(
            games_by_category_df, 
            names='Category', 
            values='Count',
            hole=0.4,
            color='Category',
            color_discrete_sequence=px.colors.sequential.Rainbow
        )
        fig_category_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_category_pie, use_container_width=True)
        
        # Bar Chart
        fig_category_bar = px.bar(
            games_by_category_df, 
            x='Count', 
            y='Category',
            orientation='h',
            text='Count',
            color='Count',
            color_continuous_scale=px.colors.sequential.Rainbow
        )
        fig_category_bar.update_traces(texttemplate='%{text}', textposition='outside')
        fig_category_bar.update_layout(
            xaxis=dict(title='Number of Searches'),
            yaxis=dict(title='Category'),
            showlegend=False,
        )
        st.plotly_chart(fig_category_bar, use_container_width=True)
    else:
        st.info("No category-based game search data available.")
    
    # Searched Games by Subcategory
    st.markdown("### Searched Games by Subcategory")
    games_by_subcategory = session.query(
        SearchedGame.subcategory, 
        func.count(SearchedGame.game_id)
    ).group_by(SearchedGame.subcategory).all()
    games_by_subcategory_df = pd.DataFrame(games_by_subcategory, columns=["Subcategory", "Count"])
    
    if not games_by_subcategory_df.empty:
        # Pie Chart
        fig_subcategory_pie = px.pie(
            games_by_subcategory_df, 
            names='Subcategory', 
            values='Count',
            hole=0.4,
            color='Subcategory',
            color_discrete_sequence=px.colors.sequential.algae
        )
        fig_subcategory_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_subcategory_pie, use_container_width=True)
        
        # Bar Chart
        fig_subcategory_bar = px.bar(
            games_by_subcategory_df, 
            x='Count', 
            y='Subcategory',
            orientation='h',
            text='Count',
            color='Count',
            color_continuous_scale=px.colors.sequential.Oranges
        )
        fig_subcategory_bar.update_traces(texttemplate='%{text}', textposition='outside')
        fig_subcategory_bar.update_layout(
            xaxis=dict(title='Number of Searches'),
            yaxis=dict(title='Subcategory'),
            showlegend=False,
        )
        st.plotly_chart(fig_subcategory_bar, use_container_width=True)
    else:
        st.info("No subcategory-based game search data available.")
    
    # Game Searches Over Time
    st.markdown("### Game Searches Over Time")
    searches_over_time = session.query(
        func.date_trunc('month', SearchedGame.searched_time).label('month'),
        func.count(SearchedGame.game_id)
    ).group_by('month').order_by('month').all()
    searches_over_time_df = pd.DataFrame(searches_over_time, columns=["Month", "Search Count"])
    searches_over_time_df['Month'] = pd.to_datetime(searches_over_time_df['Month'])
    
    if not searches_over_time_df.empty and searches_over_time_df['Search Count'].sum() > 0:
        fig_search_time = px.line(
            searches_over_time_df, 
            x='Month', 
            y='Search Count',
            markers=True,
            labels={'Month': 'Month', 'Search Count': 'Number of Searches'},
            color_discrete_sequence=px.colors.sequential.Oranges
        )
        fig_search_time.update_layout(
            xaxis=dict(
                tickformat="%b %Y",
                tickangle=-45
            ),
            yaxis=dict(tickprefix=""),
        )
        st.plotly_chart(fig_search_time, use_container_width=True)
    else:
        st.info("No game search data available.")

def chat_history_analytics(session: Session):
    """
    Displays chat history-related analytics including total chats, chats over time,
    related vs. non-related questions, and most common questions.

    Args:
        session (Session): SQLAlchemy session.
    """
    st.header("💬 Chat History Analytics")
    
    # Total Chats
    total_chats = session.query(func.count(ChatHistory.chat_id)).scalar()
    st.metric("Total Chats", int(total_chats))
    
    # Chats Over Time
    st.markdown("### Chats Over Time")
    chats_over_time = session.query(
        func.date_trunc('month', ChatHistory.timestamp).label('month'),
        func.count(ChatHistory.chat_id)
    ).group_by('month').order_by('month').all()
    chats_over_time_df = pd.DataFrame(chats_over_time, columns=["Month", "Chat Count"])
    chats_over_time_df['Month'] = pd.to_datetime(chats_over_time_df['Month'])
    
    if not chats_over_time_df.empty and chats_over_time_df['Chat Count'].sum() > 0:
        fig_chats_time = px.line(
            chats_over_time_df, 
            x='Month', 
            y='Chat Count',
            markers=True,
            labels={'Month': 'Month', 'Chat Count': 'Number of Chats'},
            color_discrete_sequence=px.colors.sequential.Oranges
        )
        fig_chats_time.update_layout(
            xaxis=dict(
                tickformat="%b %Y",
                tickangle=-45
            ),
            yaxis=dict(tickprefix=""),
        )
        st.plotly_chart(fig_chats_time, use_container_width=True)
    else:
        st.info("No chat data available.")
    
    # Related vs. Non-related Questions
    st.markdown("### Related vs. Non-related Questions")
    related_counts = session.query(
        ChatHistory.is_related, 
        func.count(ChatHistory.chat_id)
    ).group_by(ChatHistory.is_related).all()
    related_df = pd.DataFrame(related_counts, columns=["Is Related", "Count"])
    related_df['Is Related'] = related_df['Is Related'].map({True: 'Related', False: 'Not Related'})
    
    if not related_df.empty:
        # Pie Chart
        fig_related_pie = px.pie(
            related_df, 
            names='Is Related', 
            values='Count',
            hole=0.4,
            color='Is Related',
            color_discrete_sequence=px.colors.sequential.Rainbow
        )
        fig_related_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_related_pie, use_container_width=True)
        
        # Bar Chart
        fig_related_bar = px.bar(
            related_df, 
            x='Count', 
            y='Is Related',
            orientation='h',
            text='Count',
            color='Count',
            color_continuous_scale=px.colors.sequential.Viridis
        )
        fig_related_bar.update_traces(texttemplate='%{text}', textposition='outside')
        fig_related_bar.update_layout(
            xaxis=dict(title='Number of Questions'),
            yaxis=dict(title='Question Type'),
            showlegend=False,
        )
        st.plotly_chart(fig_related_bar, use_container_width=True)
    else:
        st.info("No related/non-related question data available.")
    
    # Most Common Questions
    st.markdown("### Top 10 Most Common Questions")
    common_questions = session.query(
        ChatHistory.question, 
        func.count(ChatHistory.chat_id).label('Count')
    ).group_by(ChatHistory.question)\
     .order_by(func.count(ChatHistory.chat_id).desc())\
     .limit(10)\
     .all()
    common_questions_df = pd.DataFrame(common_questions, columns=["Question", "Count"])
    
    if not common_questions_df.empty:
        fig_common_questions = px.bar(
            common_questions_df, 
            x='Count', 
            y='Question',
            orientation='h',
            text='Count',
            color='Count',
            color_continuous_scale=px.colors.sequential.Purples
        )
        fig_common_questions.update_traces(texttemplate='%{text}', textposition='outside')
        fig_common_questions.update_layout(
            xaxis=dict(title='Number of Times Asked'),
            yaxis=dict(title='Question'),
            showlegend=False,
        )
        st.plotly_chart(fig_common_questions, use_container_width=True)
    else:
        st.info("No question data available.")

def search_performance_metrics(session: Session):
    """
    Displays search performance metrics including Hit Rate@10 and MRR@10 for various search methods.

    Args:
        session (Session): SQLAlchemy session.
    """
    st.header("🔍 Search Performance Metrics")
    
    # Data Preparation
    data = {
        "Search Method": [
            "Text Search with MINSEARCH",
            "Text Search with Boosting",
            "Vector Search with Weaviate",
            "Hybrid Search",
            "Document Reranking"
        ],
        "Hit Rate@10": [
            0.5519,
            0.8146,
            0.9515,
            0.9715,
            0.9715
        ],
        "MRR@10": [
            0.2861,
            0.5880,
            0.7799,
            0.8177,
            0.8146
        ]
    }

    df = pd.DataFrame(data)

    # Display the DataFrame with visible tables using st.dataframe for better styling
    st.markdown("### Key Metrics")
    styled_table = df.style.format({
        "Hit Rate@10": "{:.2%}", 
        "MRR@10": "{:.2%}"
    }).set_table_styles([
        {'selector': 'th', 'props': [('background-color', '#f2f2f2'), ('text-align', 'center'), ('font-size', '16px')]},
        {'selector': 'td', 'props': [('text-align', 'center'), ('font-size', '14px')]}
    ])
    st.dataframe(styled_table, use_container_width=True)
    
    # Hit Rate Comparison
    st.markdown("### 📊 Hit Rate Comparison")
    fig_hit = px.bar(
        df,
        x="Search Method",
        y="Hit Rate@10",
        text="Hit Rate@10",
        color="Hit Rate@10",
        color_continuous_scale=px.colors.sequential.Greens,
        labels={"Hit Rate@10": "Hit Rate@10"},
        height=300
    )
    fig_hit.update_traces(texttemplate='%{text:.2%}', textposition='inside')
    fig_hit.update_layout(
        uniformtext_minsize=8,
        uniformtext_mode='hide',
        xaxis_title="Search Method",
        yaxis_title="Hit Rate@10",
        showlegend=False
    )
    st.plotly_chart(fig_hit, use_container_width=True)
    
    # MRR Comparison
    st.markdown("### 📈 Mean Reciprocal Rank (MRR) Comparison")
    fig_mrr = px.bar(
        df,
        x="Search Method",
        y="MRR@10",
        text="MRR@10",
        color="MRR@10",
        color_continuous_scale=px.colors.sequential.OrRd,
        labels={"MRR@10": "MRR@10"},
        height=300
    )
    fig_mrr.update_traces(texttemplate='%{text:.2%}', textposition='inside')
    fig_mrr.update_layout(
        uniformtext_minsize=8,
        uniformtext_mode='hide',
        xaxis_title="Search Method",
        yaxis_title="MRR@10",
        showlegend=False
    )
    st.plotly_chart(fig_mrr, use_container_width=True)

    # Combined Metrics
    st.markdown("### 📊 Combined Hit Rate and MRR")
    fig_combined = px.scatter(
        df,
        x="Hit Rate@10",
        y="MRR@10",
        text="Search Method",
        size="Hit Rate@10",
        color="MRR@10",
        color_continuous_scale=px.colors.sequential.Greens,
        labels={"Hit Rate@10": "Hit Rate@10", "MRR@10": "MRR@10"},
        height=400
    )
    fig_combined.update_traces(textposition='top center')
    fig_combined.update_layout(
        showlegend=False,
        xaxis=dict(
            tickformat=".0%",
            title="Hit Rate@10",
            titlefont=dict(size=18)
        ),
        yaxis=dict(
            tickformat=".0%",
            title="MRR@10",
            titlefont=dict(size=18)
        )
    )
    st.plotly_chart(fig_combined, use_container_width=True)

    # Highlight Best Performers
    st.markdown("### 🏆 Best Performing Search Methods")
    best_hit_rate = df.loc[df["Hit Rate@10"] == df["Hit Rate@10"].max()]
    best_mrr = df.loc[df["MRR@10"] == df["MRR@10"].max()]
    best_methods = pd.concat([best_hit_rate, best_mrr]).drop_duplicates()
    
    if not best_methods.empty:
        styled_best_methods = best_methods.style.format({
            "Hit Rate@10": "{:.2%}", 
            "MRR@10": "{:.2%}"
        }).set_table_styles([
            {'selector': 'th', 'props': [('background-color', '#f2f2f2'), ('text-align', 'center'), ('font-size', '16px')]},
            {'selector': 'td', 'props': [('text-align', 'center'), ('font-size', '14px')]}
        ])
        st.dataframe(styled_best_methods, use_container_width=True)
    else:
        st.info("No best performing search methods to display.")
    
    st.markdown("""
    ---
    *This dashboard provides an overview of the search performance metrics for the Game Finder project. The metrics include Hit Rate@10 and Mean Reciprocal Rank (MRR@10) for various search methods.*
    """)

