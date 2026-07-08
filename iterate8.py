def is_cell_in_any_path(pending_moves, r, c):
    for move in pending_moves:
        r_src, c_src = move["from_cell"]
        r_to, c_to = move["to_cell"]
        
        # אם המשבצת היא המקור או היעד של כלי אחר שנוסע
        if (r, c) == (r_src, c_src) or (r, c) == (r_to, c_to):
            return True
            
        # בדיקה אם המשבצת נמצאת באמצע המסלול (לכלים שנעים בקווים ישרים או אלכסונים)
        # נבדוק קודם כל אם r ו-c נמצאים בטווח הכללי שבין ה-src ל-to
        if min(r_src, r_to) <= r <= max(r_src, r_to) and min(c_src, c_to) <= c <= max(c_src, c_to):
            # 1. תנועה אופקית (כמו המלכה בטסט: r_src == r_to)
            if r_src == r_to == r:
                return True
            # 2. תנועה אנכית
            if c_src == c_to == c:
                return True
            # 3. תנועה אלכסונית (הפרש השורות שווה להפרש העמודות)
            if abs(r - r_src) == abs(c - c_src) and abs(r_to - r_src) == abs(c_to - c_src):
                # ודא שהכיוון הלוגי מתאים (שהיא לא בפינה הנגדית)
                step_r = 1 if r_to > r_src else -1
                step_c = 1 if c_to > c_src else -1
                # בדיקה אם היחס של הצעדים שווה
                if (r - r_src) * step_r > 0 and (c - c_src) * step_c > 0:
                    return True
    return False