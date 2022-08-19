from eprogress import LineProgress, CircleProgress, MultiProgressManager
# circle loading
    circle_progress = CircleProgress(title='circle loading')
    for i in range(1, 101):
        circle_progress.update(i)
        time.sleep(0.1)

# line progress
        line_progress = LineProgress(title='line progress')
        for i in range(1, 101):
            line_progress.update(i)
            time.sleep(0.05)
# multi line or circle loading progress
progress_manager = MultiProgressManager()
progress_manager.put(str(1001), LineProgress(total=100, title='1 thread'))
progress_manager.put(str(1002), LineProgress(total=100, title='2 thread'))
progress_manager.put(str(1003), LineProgress(total=100, title='3 thread'))
progress_manager.put(str(1004), CircleProgress(title='4 thread'))

progress_manager.update(key, progress)