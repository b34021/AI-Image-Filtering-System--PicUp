"""
בנייה ועיבוד דמויות
"""
import os
from typing import Dict, Any, List
from services.burnt import Burnt
from services.sharpness import Sharpness
burnt = Burnt()
sharpness = Sharpness()
class Build:

    def build_event_images(self, path: str, cust_id: int, event_id: int) -> Dict[str, Any]:
        """
        בנה דמויות לאירוע ספציפי של לקוח
        עבור על כל תמונה, חשב את ציון burnt וחזר עם רשימה של ניתוב וציון

        :param path: נתיב לתיקיית התמונות
        :param cust_id: מזהה הלקוח
        :param event_id: מזהה האירוע
        :return: dict עם תוצאות העיבוד וציוני burnt עבור כל תמונה
        """

        # בדיקה שהנתיב קיים
        if not os.path.exists(path):
            return {
                "status": "error",
                "message": f"הנתיב לא קיים: {path}",
                "cust_id": cust_id,
                "event_id": event_id
            }

        # בדיקה שהנתיב הוא תיקייה
        if not os.path.isdir(path):
            return {
                "status": "error",
                "message": f"הנתיב אינו תיקייה: {path}",
                "cust_id": cust_id,
                "event_id": event_id
            }

        # קבלת רשימת התמונות
        try:
            images = [f for f in os.listdir(path) 
                      if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp'))]
        except Exception as e:
            return {
                "status": "error",
                "message": f"שגיאה בקריאת התיקייה: {str(e)}",
                "cust_id": cust_id,
                "event_id": event_id
            }

        # עיבוד כל תמונה וחישוב ציון burnt
        mark_results: List[Dict[str, Any]] = []
        
        for image in images:
            full_path = os.path.join(path, image)
            try:
                burnt_score_value = burnt.burnt_score(image_path=full_path)
                sharpness_value = sharpness.calculate_sharpness_laplacian(image_path=full_path)
                mark_results.append({
                    "image_path": full_path,
                    "image_name": image,
                    "burnt_score": burnt_score_value,
                    "sharpness_score": sharpness_value
                })

            except Exception as e:
                mark_results.append({
                    "image_path": full_path,
                    "image_name": image,
                    "burnt_score": None,
                    "sharpness_score": None,
                    "error": str(e)
                })
            

        # בנייה וחזרה של התוצאות
        return mark_results
