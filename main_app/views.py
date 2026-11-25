from django.shortcuts import render
from .recommender import courses, recommend_courses

# Create your views here.


def index(request):
    courses = [
        {'name': 'Data', 'platforms': 71},
        {'name': 'Management', 'platforms': 53},
        {'name': 'Science', 'platforms': 44},
        {'name': 'Business', 'platforms': 43},
        {'name': 'Learning', 'platforms': 39},
        {'name': 'Health', 'platforms': 35},
        {'name': 'Python', 'platforms': 35},
        {'name': 'Fundamentals', 'platforms': 32},
        {'name': 'Design', 'platforms': 30},
        {'name': 'Cloud', 'platforms': 29},
        {'name': 'Google', 'platforms': 29},
        {'name': 'Development', 'platforms': 25},
        {'name': 'Machine', 'platforms': 24},
        {'name': 'English', 'platforms': 24},
        {'name': 'Programming', 'platforms': 23},
        {'name': 'Strategy', 'platforms': 20},
        {'name': 'Foundations', 'platforms': 19},
        {'name': 'Global', 'platforms': 19},
        {'name': 'Social', 'platforms': 19},
        {'name': 'Analysis', 'platforms': 19},
        {'name': 'Marketing', 'platforms': 19},
        {'name': 'Financial', 'platforms': 18},
        {'name': 'Skills', 'platforms': 17},
        {'name': 'Digital', 'platforms': 17},
        {'name': 'International', 'platforms': 17},
    ]

    return render(request, 'index.html', {
        'courses': courses,
    })




def search_courses(request):
    keyword = request.GET.get('keyword', '').strip()

    matching_courses = []

    if keyword:
        results = courses[
            courses['course_title'].str.contains(
                keyword,
                case=False,
                na=False,
                regex=False
            )
        ].head(20)

        matching_courses = [
            {
                'course_id': index,
                'course_title': row['course_title'],
                'organization': row['course_organization'],
                'difficulty': row['course_difficulty'],
            }
            for index, row in results.iterrows()
        ]

    return render(request, 'search_results.html', {
        'keyword': keyword,
        'matching_courses': matching_courses,
    })




def course_recommendations(request, course_id):
    selected_course = courses.iloc[course_id]

    recommendations = recommend_courses(course_id)

    return render(request, 'recommendations.html', {
        'selected_course': selected_course,
        'recommendations': recommendations,
    })