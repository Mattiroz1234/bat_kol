@@ .. @@
 export interface FeedbackData {
   actor_id: string;
   target_id: string;
-  status: 'likes' | 'dislikes' | 'waiting';
+  status: 'likes' | 'dislikes';
 }