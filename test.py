answer.edited_at = datetime.utcnow()
        utc_time = answer.edited_at
        pacific_time = pytz.timezone('US/Pacific')
        utc = pytz.utc
        local_time = utc.localize(utc_time).astimezone(pacific_time)



mine: 2017-07-05 01:21:17.045781+00
reddit: 2017-01-03 05:30:18+00

dom try: 2017-01-25 22:37:48.100000
1483315661
        converted_utc = datetime.utcfromtimestamp(float(1483315661))


Thursday 06, July 2017 10:30PM        


user_id = session.get("user_id")
    if not user_id:
        raise Exception("No user logged in.")

    question = Question.query.get(question_id)


    answer = request.form.get("user_answer")
    if answer:
        new_answer = Answer(user_id=user_id, question_id=question_id, body=answer)
        flash("Answer added.")
        db.session.add(new_answer)
        db.session.commit()

        the_time = question.created_at.ctime()

        return render_template('question_info_page.html', 
                        question=question, answer=new_answer, created_at=the_time)


    edited_answer = request.form.get("updated_answer")
    if edited_answer:

        answer = Answer.query.filter(Answer.user_id == user_id, Answer.question_id == question_id).one()
        answer.body = edited_answer

        flash("Answer updated.")
        db.session.commit()

        the_time = question.created_at.ctime()

        return render_template('question_info_page.html', 
                        question=question, answer=answer.body, created_at=the_time)
