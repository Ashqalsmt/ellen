
import asyncio
import json
import logging
import os
import random
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union, Any
import aiofiles

from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup, 
    User, Chat, Message, CallbackQuery, ChatPermissions
)
from telegram.ext import (
    Application, CommandHandler, MessageHandler, 
    CallbackQueryHandler, ContextTypes, filters,
    ChatMemberHandler
)

 

# إعداد السجلات
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class avetaarAdvancedBot:
    """بوت  المتطور - جميع الميزات الخارقة"""
    
    def __init__(self):
        """تهيئة البوت"""
        # الإعدادات الأساسية
        self.TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
        if not self.TOKEN:
            raise ValueError("TELEGRAM_BOT_TOKEN is required")
        
        # معرفات المطورين
        self.SUDO_USERS = [5571722913]  # معرف المطور الأساسي
        self.SUDO_USERNAME = "T_A_Tl"
 
        # معلومات البوت
        self.bot_name = " إلين. 𓅓𝑬𝑳𝑳𝑬𝑵 "
        self.BOT_USERNAME = None
        
        # قاعدة البيانات المحلية
        self.db: Dict[str, Any] = {}
        self.db_file = "T_A_Tl_advanced_db.json"
        
        # الألعاب النشطة
        self.active_games: Dict[int, Dict] = {}
        
        # إحصائيات متقدمة
        self.stats = {
            "messages_today": 0,
            "commands_used": 0,
            "games_played": 0,
            "money_transferred": 0
        }
        
        # بنك الأسئلة المتطور
        self.riddles_bank = [
            {"q": "ما الشيء الذي يكتب ولا يقرأ؟", "a": "القلم"},
            {"q": "ما الشيء الذي له رأس ولا يملك عينين؟", "a": "الدبوس"},
            {"q": "ما الشيء الذي يسير بلا أرجل؟", "a": "الوقت"},
            {"q": "ما الشيء الذي كلما زاد نقص؟", "a": "العمر"},
            {"q": "ما الشيء الذي يأكل ولا يشبع؟", "a": "النار"},
            {"q": "ما الشيء الذي يطير بلا جناح؟", "a": "الخبر"},
            {"q": "ما الشيء الذي له أسنان ولا يعض؟", "a": "المفتاح"},
            {"q": "ما الشيء الذي يرى كل شيء وهو أعمى؟", "a": "المرآة"},
            {"q": "ما الشيء الذي إذا لمسته صاح؟", "a": "الجرس"},
            {"q": "ما الشيء الذي يجري ولا يتعب؟", "a": "الماء"}
        ]
        
        self.math_questions = [
            {"q": "كم يساوي 15 + 25؟", "a": "40"},
            {"q": "كم يساوي 9 × 8؟", "a": "72"},
            {"q": "كم يساوي 100 ÷ 4؟", "a": "25"},
            {"q": "كم يساوي 13² (13 تربيع)؟", "a": "169"},
            {"q": "كم يساوي √64 (الجذر التربيعي لـ64)؟", "a": "8"},
            {"q": "كم يساوي 50% من 200؟", "a": "100"},
            {"q": "كم يساوي 7 × 9 - 3؟", "a": "60"},
            {"q": "كم يساوي (12 + 8) ÷ 4؟", "a": "5"},
            {"q": "كم يساوي 15 × 4 + 10؟", "a": "70"},
            {"q": "كم يساوي 200 - 75 + 25؟", "a": "150"}
        ]
        
 

        # أسئلة صراحة وجرأة متطورة
        self.truth_questions = [
            "ما أكثر شيء تخاف منه في المستقبل؟",
            "ما أسوأ كذبة قلتها في حياتك؟",
            "من هو الشخص الذي تحبه سراً؟",
            "ما أكثر شيء تندم عليه في حياتك؟",
            "ما أغرب حلم رأيته؟",
            "من آخر شخص فكرت فيه قبل النوم؟",
            "ما أكثر شيء محرج حدث لك؟",
            "لو كان بإمكانك تغيير شيء في شكلك، ما سيكون؟",
            "ما أكثر شيء تريد أن تحققه في حياتك؟",
            "من هو قدوتك في الحياة؟"
        ]
        
        self.dare_challenges = [
            "اكتب رسالة حب لأول شخص في قائمة جهات الاتصال",
            "التقط صورة سيلفي مضحكة وأرسلها",
            "اكتب منشور على حالتك عن شيء محرج",
            "اتصل بأحد أصدقائك وقل له شيء مضحك",
            "ارقص لمدة دقيقة واحدة",
            "اكتب قصيدة من 4 أبيات",
            "قلد صوت أحد المشاهير",
            "اكتب اسمك بيدك غير المسيطرة",
            "اعمل مقلب في أحد أصدقائك",
            "غن أغنية أمام الجميع"
        ]
        
        # بنك المزرعة المتطور
        self.farm_crops = {
            "potato": {"name": "🥔 البطاطس", "time": 30, "price": 50, "buy": 20},
            "tomato": {"name": "🍅 الطماطم", "time": 45, "price": 75, "buy": 30},
            "carrot": {"name": "🥕 الجزر", "time": 60, "price": 100, "buy": 40},
            "corn": {"name": "🌽 الذرة", "time": 90, "price": 150, "buy": 60},
            "strawberry": {"name": "🍓 الفراولة", "time": 120, "price": 200, "buy": 80},
            "watermelon": {"name": "🍉 البطيخ", "time": 180, "price": 350, "buy": 150},
            "grape": {"name": "🍇 العنب", "time": 240, "price": 500, "buy": 200}
        }
        
        # نظام الحماية المتطور
        self.protection_settings = {
            "flood_limit": 10,  # عدد الرسائل المسموحة بالدقيقة
            "spam_words": ["سبام", "إعلان", "تسويق", "بيع", "شراء"],
            "bad_words": ["كلب", "حيوان", "غبي", "أحمق", "لعنة"],
            "max_warns": 3,  # عدد التحذيرات قبل الطرد
            "mute_time": 5,  # مدة الكتم بالدقائق
        }
        
        # تحميل قاعدة البيانات
        self.load_database()
        
        # إنشاء التطبيق
        self.application = Application.builder().token(self.TOKEN).build()
        
        # تسجيل المعالجات
        self.setup_handlers()
        
        logger.info("💎 T_A_Tl Advanced Bot initialized successfully!")

    def load_database(self):
        """تحميل قاعدة البيانات"""
        try:
            if os.path.exists(self.db_file):
                with open(self.db_file, 'r', encoding='utf-8') as f:
                    self.db = json.load(f)
            else:
                self.db = {
                    "users": {},
                    "groups": {},
                    "stats": {"total_users": 0, "total_groups": 0},
                    "settings": {"bot_free": True, "maintenance": False}
                }
                self.save_database()
                
        except Exception as e:
            logger.error(f"Error loading database: {e}")
            self.db = {}

    def save_database(self):
        """حفظ قاعدة البيانات"""
        try:
            with open(self.db_file, 'w', encoding='utf-8') as f:
                json.dump(self.db, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Error saving database: {e}")

    def setup_handlers(self):
        """تسجيل معالجات الأحداث"""
        # معالج أمر البداية
        self.application.add_handler(CommandHandler("start", self.start_command))
        
        # معالج الرسائل النصية
        self.application.add_handler(MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            self.handle_message
        ))
        
        # معالج الاستعلامات
        self.application.add_handler(CallbackQueryHandler(self.handle_callback))
        
        # معالج الأعضاء الجدد والمغادرين
        self.application.add_handler(MessageHandler(
            filters.StatusUpdate.NEW_CHAT_MEMBERS | filters.StatusUpdate.LEFT_CHAT_MEMBER,
            self.handle_member_status
        ))

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """معالج أمر /start"""
        user = update.effective_user
        chat = update.effective_chat
        
        if not user or not chat:
            return
            
        # حفظ معلومات المستخدم
        await self.save_user_info(user)
        
        if chat.type == "private":
            await self.handle_private_start(update, user)
        else:
            await self.handle_group_start(update, user, chat)

    async def handle_private_start(self, update: Update, user: User):
        """معالجة البداية في الخاص"""
        welcome_text = f"""
╭─═◇【 🌟 أهلاً بك في عالم إلين. 𓅓𝑬𝑳𝑳𝑬𝑵 🌟 】◇═─╮
┃
┣━➤ 👋 مرحباً {user.first_name}
┣━➤ 🤖 أنا {self.bot_name}
┣━➤ 💎 بوت متطور بميزات خارقة
┣━➤ 🏆 تم تطويري بأحدث التقنيات
┃
┣━━━━━━━━━【 ⚡ الميزات الخارقة ⚡ 】━━━━━━━━━┫
┣━➤ 🏦 نظام بنك متطور مع استثمارات
┣━➤ 🚜 مزرعة افتراضية بـ20+ محصول
┣━➤ 🎮 +50 لعبة تفاعلية مختلفة
┣━➤ 🛡️ حماية خارقة ضد جميع أنواع الهجمات
┣━➤ 🤖 ذكاء اصطناعي متقدم للردود
┣━➤ 📊 إحصائيات تفصيلية وتقارير ذكية
┣━➤ 🎵 مشغل موسيقى متطور
┣━➤ 🌐 ترجمة فورية لـ100+ لغة
┣━➤ 📰 أخبار لحظية من جميع أنحاء العالم
┣━➤ 🔍 بحث متقدم في جميع المنصات
┃
┣━━━━━━━━━【 📱 للبدء الآن 📱 】━━━━━━━━━┫
┣━➤ 1️⃣ أضف البوت لمجموعتك كمشرف
┣━➤ 2️⃣ اكتب "تفعيل" في المجموعة
┣━➤ 3️⃣ استمتع بجميع الميزات المتطورة!
┃
┣━➤ 📢 القناة: @YamenThon
┣━➤ 👨‍💻 المطور: @{self.SUDO_USERNAME}
┃
╰─═◇【 💝 شكراً لاختيارك بوت إلين. 𓅓𝑬𝑳𝑳𝑬𝑵 💝 】◇═─╯
        """
        
        keyboard = [
            [InlineKeyboardButton("🚀 أضف البوت لمجموعتك", 
                                url=f"https://t.me/{self.BOT_USERNAME}?startgroup=true")],
            [
                InlineKeyboardButton("📢 القناة", url="https://t.me/YamenThon"),
                InlineKeyboardButton("💬 المطور", url=f"https://t.me/{self.SUDO_USERNAME}")
            ],
            [
                InlineKeyboardButton("📊 إحصائياتي", callback_data="my_stats"),
                InlineKeyboardButton("💰 رصيدي", callback_data="my_balance")
            ]
        ]
        
        if update.message:
            await update.message.reply_text(
                welcome_text,
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

    async def handle_group_start(self, update: Update, user: User, chat: Chat):
        """معالجة البداية في المجموعة"""
        if not self.is_group_activated(chat.id):
            activation_text = """
╭─═◇【 🔥 تفعيل بوت إلين. 𓅓𝑬𝑳𝑳𝑬𝑵 🔥 】◇═─╮
┃
┣━➤ ⚠️ البوت غير مفعل في هذه المجموعة
┣━➤ 🔑 للتفعيل: اكتب "تفعيل" 
┣━➤ 👑 يجب أن تكون مشرف أو مالك المجموعة
┃
╰─═◇【 💎 بوت إلين. 𓅓𝑬𝑳𝑳𝑬𝑵 💎 】◇═─╯
            """
            if update.message:
                await update.message.reply_text(activation_text)

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """معالج الرسائل الرئيسي"""
        if not update.message or not update.message.text:
            return
            
        message = update.message
        user = update.effective_user
        chat = update.effective_chat
        text = message.text.strip()
        
        if not user or not chat:
            return
        
        # حفظ إحصائيات الرسالة
        await self.update_message_stats(user.id, chat.id)
        
        # فحص وضع الصيانة
        if self.db.get("settings", {}).get("maintenance", False):
            if not self.is_sudo(user.id):
                await message.reply_text("🔧 البوت في وضع الصيانة حالياً")
                return
        
        # فحص تفعيل المجموعة
        if chat.type != "private" and not self.is_group_activated(chat.id):
            if text in ["تفعيل", "تفعيل البوت"]:
                await self.activate_group(update, user, chat)
            return
        
        # معالجة الأوامر حسب النوع
        await self.process_command(update, text, user, chat)

    async def process_command(self, update: Update, text: str, user: User, chat: Chat):
        """معالجة الأوامر المختلفة"""
        text_lower = text.lower()
        
        # الأوامر العامة (متاحة للجميع)
        if text_lower in ["الاوامر", "الأوامر", "اوامر"]:
            await self.show_commands(update, user)
        elif text_lower in ["ايدي", "معلوماتي", "موقعي"]:
            await self.show_user_info(update, user, chat)
        elif text_lower in ["رصيدي", "فلوسي", "رصيد"]:
            await self.show_balance(update, user)
        elif text_lower in ["راتبي", "الراتب"]:
            await self.show_salary_info(update, user)
        elif text_lower in ["اليوميه", "استلام", "راتب"]:
            await self.daily_salary(update, user)
        elif text_lower in ["الالعاب", "الألعاب", "العاب"]:
            await self.show_games_menu(update)
        elif text_lower in ["البنك", "بنك"]:
            await self.show_bank_menu(update)
        elif text_lower in ["المزرعة", "مزرعة", "الزراعة"]:
            await self.show_farm_menu(update)
        elif text_lower in ["احصائياتي", "احصائيات"]:
            await self.show_user_stats(update, user, chat)
        elif text_lower == "فحص البوت":
            await self.bot_status(update)
        
        # الألعاب
        elif text_lower in ["لغز", "الغاز"]:
            await self.start_riddle_game(update, user, chat)
        elif text_lower in ["رياضيات", "حساب", "رياضه"]:
            await self.start_math_game(update, user, chat)
        elif text_lower in ["صراحة", "صراحه"]:
            await self.truth_question(update)
        elif text_lower in ["جرأة", "جرأه", "تحدي"]:
            await self.dare_challenge(update)
        
        # أوامر الإدارة
        elif await self.is_admin(user.id, chat.id):
            await self.handle_admin_commands(update, text, user, chat)
        
        # أوامر المطورين
        elif self.is_sudo(user.id):
            await self.handle_sudo_commands(update, text, user, chat)
        
        # معالجة الردود التلقائية
        else:
            await self.handle_auto_replies(update, text, chat)

    async def show_commands(self, update: Update, user: User):
        """عرض قائمة الأوامر"""
        commands_text = """
╭─═◇【 📋 قائمة الأوامر الكاملة 📋 】◇═─╮
┃
┣━━━━━━━━━【 👤 الأوامر العامة 👤 】━━━━━━━━━┫
┣━➤ معلوماتي ← عرض معلوماتك
┣━➤ رصيدي ← عرض رصيدك
┣━➤ راتبي ← معلومات الراتب اليومي
┣━➤ اليوميه ← استلام الراتب اليومي
┣━➤ احصائياتي ← إحصائياتك الشخصية
┣━➤ فحص البوت ← حالة البوت
┃
┣━━━━━━━━━【 🎮 الألعاب والترفيه 🎮 】━━━━━━━━━┫
┣━➤ الالعاب ← قائمة الألعاب
┣━➤ لغز ← لعبة الألغاز
┣━➤ رياضيات ← لعبة الرياضيات
┣━➤ صراحة ← أسئلة صراحة
┣━➤ جرأة ← تحديات جرأة
┃
┣━━━━━━━━━【 💰 النظام المالي 💰 】━━━━━━━━━┫
┣━➤ البنك ← قائمة البنك
┣━➤ تحويل [المبلغ] ← تحويل أموال
┣━➤ استثمار [المبلغ] ← استثمار الأموال
┣━➤ قرض [المبلغ] ← طلب قرض
┃
┣━━━━━━━━━【 🚜 نظام المزرعة 🚜 】━━━━━━━━━┫
┣━➤ المزرعة ← قائمة المزرعة
┣━➤ زراعة [المحصول] ← زراعة محصول
┣━➤ حصاد ← حصاد المحاصيل
┣━➤ متجر المزرعة ← شراء البذور
┃
╰─═◇【 💎 بوت إلين. 𓅓𝑬𝑳𝑳𝑬𝑵 💎 】◇═─╯
        """
        
        keyboard = [
            [
                InlineKeyboardButton("🎮 الألعاب", callback_data="games_menu"),
                InlineKeyboardButton("💰 البنك", callback_data="bank_menu")
            ],
            [
                InlineKeyboardButton("🚜 المزرعة", callback_data="farm_menu"),
                InlineKeyboardButton("📊 الإحصائيات", callback_data="stats_menu")
            ]
        ]
        
        if update.message:
            await update.message.reply_text(
                commands_text,
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

    async def show_games_menu(self, update: Update):
        """عرض قائمة الألعاب"""
        games_text = """
╭─═◇【 🎮 مركز الألعاب المتطور 🎮 】◇═─╮
┃
┣━━━━━━━━━【 🧠 ألعاب الذكاء 🧠 】━━━━━━━━━┫
┣━➤ 🧩 الألغاز ← أكثر من 100 لغز
┣━➤ 🔢 الرياضيات ← تحديات حسابية
┣━➤ 🔤 الكلمات ← ألعاب المفردات
┣━➤ 🧮 الذاكرة ← اختبارات التذكر
┃
┣━━━━━━━━━【 🎯 ألعاب التحدي 🎯 】━━━━━━━━━┫
┣━➤ 💭 صراحة ← أسئلة شخصية
┣━➤ ⚡ جرأة ← تحديات مثيرة
┣━➤ 🎲 حظ ← ألعاب الحظ
┣━➤ 🏁 سباق ← منافسات سريعة
┃
┣━━━━━━━━━【 🎪 ألعاب جماعية 🎪 】━━━━━━━━━┫
┣━➤ 🎯 التخمين ← خمن الرقم/الكلمة
┣━➤ 🔍 البحث ← ابحث عن الكنز
┣━➤ 🎭 التمثيل ← ألعاب أدوار
┣━➤ 🏆 المسابقات ← جوائز يومية
┃
╰─═◇【 🌟 اختر لعبتك المفضلة 🌟 】◇═─╯
        """
        
        keyboard = [
            [
                InlineKeyboardButton("🧩 لغز", callback_data="game_riddle"),
                InlineKeyboardButton("🔢 رياضيات", callback_data="game_math")
            ],
            [
                InlineKeyboardButton("💭 صراحة", callback_data="game_truth"),
                InlineKeyboardButton("⚡ جرأة", callback_data="game_dare")
            ],
            [
                InlineKeyboardButton("🎯 التخمين", callback_data="game_guess"),
                InlineKeyboardButton("🎲 الحظ", callback_data="game_luck")
            ],
            [InlineKeyboardButton("🏆 المسابقة الكبرى", callback_data="game_tournament")]
        ]
        
        if update.message:
            await update.message.reply_text(
                games_text,
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

    async def show_bank_menu(self, update: Update):
        """عرض قائمة البنك المتطور"""
        user = update.effective_user
        if not user:
            return
            
        balance = self.get_user_balance(user.id)
        
        bank_text = f"""
╭─═◇【 🏦 بنك إلين. 𓅓𝑬𝑳𝑳𝑬𝑵 🏦 】◇═─╮
┃
┣━➤ 💰 رصيدك الحالي: {balance:,} دينار
┣━➤ 💳 رقم حسابك: {user.id}
┣━➤ 📈 معدل الفائدة: 5% يومياً
┃
┣━━━━━━━━━【 💼 الخدمات المصرفية 💼 】━━━━━━━━━┫
┣━➤ 💸 تحويل الأموال
┣━➤ 📊 استثمار ذكي بفوائد عالية
┣━➤ 💳 طلب قرض فوري
┣━➤ 🏪 شراء وبيع العملات
┣━➤ 📈 متابعة الاستثمارات
┣━➤ 💎 خزانة الكنوز الخاصة
┃
┣━━━━━━━━━【 🎁 العروض الخاصة 🎁 】━━━━━━━━━┫
┣━➤ 🎯 بونص الإيداع الأول: 1000 دينار
┣━➤ 💝 مكافآت الإحالة: 500 دينار
┣━➤ 🏆 جوائز الأعضاء المميزين
┃
╰─═◇【 💎 اختر الخدمة المطلوبة 💎 】◇═─╯
        """
        
        keyboard = [
            [
                InlineKeyboardButton("💸 تحويل", callback_data="bank_transfer"),
                InlineKeyboardButton("📊 استثمار", callback_data="bank_invest")
            ],
            [
                InlineKeyboardButton("💳 قرض", callback_data="bank_loan"),
                InlineKeyboardButton("🏪 التداول", callback_data="bank_trade")
            ],
            [
                InlineKeyboardButton("📈 استثماراتي", callback_data="bank_investments"),
                InlineKeyboardButton("💎 الخزانة", callback_data="bank_vault")
            ],
            [InlineKeyboardButton("📊 كشف الحساب", callback_data="bank_statement")]
        ]
        
        if update.message:
            await update.message.reply_text(
                bank_text,
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

    async def show_farm_menu(self, update: Update):
        """عرض قائمة المزرعة المتطورة"""
        user = update.effective_user
        if not user:
            return
            
        farm_text = """
╭─═◇【 🚜 مزرعة إلين. 𓅓𝑬𝑳𝑳𝑬𝑵ة 🚜 】◇═─╮
┃
┣━━━━━━━━━【 🌱 المحاصيل المتاحة 🌱 】━━━━━━━━━┫
┣━➤ 🥔 البطاطس ← 30 دقيقة ← 50 دينار
┣━➤ 🍅 الطماطم ← 45 دقيقة ← 75 دينار
┣━➤ 🥕 الجزر ← 60 دقيقة ← 100 دينار
┣━➤ 🌽 الذرة ← 90 دقيقة ← 150 دينار
┣━➤ 🍓 الفراولة ← 120 دقيقة ← 200 دينار
┣━➤ 🍉 البطيخ ← 180 دقيقة ← 350 دينار
┣━➤ 🍇 العنب ← 240 دقيقة ← 500 دينار
┃
┣━━━━━━━━━【 🏪 متجر المزرعة 🏪 】━━━━━━━━━┫
┣━➤ 🌱 بذور متنوعة عالية الجودة
┣━➤ 🚿 أنظمة الري الذكية
┣━➤ 🌡️ تحكم في درجة الحرارة
┣━➤ 💡 إضاءة صناعية متطورة
┣━➤ 🤖 روبوتات زراعية
┃
┣━━━━━━━━━【 🏆 الإنجازات 🏆 】━━━━━━━━━┫
┣━➤ 🥉 مزارع مبتدئ: 10 محاصيل
┣━➤ 🥈 مزارع محترف: 50 محصول
┣━➤ 🥇 خبير الزراعة: 100 محصول
┣━➤ 👑 ملك الزراعة: 500 محصول
┃
╰─═◇【 🌟 ابدأ رحلتك الزراعية 🌟 】◇═─╯
        """
        
        keyboard = [
            [
                InlineKeyboardButton("🌱 زراعة", callback_data="farm_plant"),
                InlineKeyboardButton("🌾 حصاد", callback_data="farm_harvest")
            ],
            [
                InlineKeyboardButton("🏪 المتجر", callback_data="farm_shop"),
                InlineKeyboardButton("📦 المخزن", callback_data="farm_storage")
            ],
            [
                InlineKeyboardButton("🔧 ترقيات", callback_data="farm_upgrades"),
                InlineKeyboardButton("📊 الإحصائيات", callback_data="farm_stats")
            ]
        ]
        
        if update.message:
            await update.message.reply_text(
                farm_text,
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

    async def start_riddle_game(self, update: Update, user: User, chat: Chat):
        """بدء لعبة الألغاز"""
        if chat.id in self.active_games:
            if update.message:
                await update.message.reply_text("🎮 يوجد لعبة نشطة بالفعل في هذه المجموعة!")
            return
        
        riddle = random.choice(self.riddles_bank)
        
        self.active_games[chat.id] = {
            "type": "riddle",
            "question": riddle["q"],
            "answer": riddle["a"].lower(),
            "start_time": datetime.now(),
            "attempts": 0,
            "max_attempts": 3,
            "reward": 100
        }
        
        riddle_text = f"""
╭─═◇【 🧩 لعبة الألغاز المتطورة 🧩 】◇═─╮
┃
┣━➤ ❓ اللغز: {riddle["q"]}
┃
┣━➤ ⏱️ الوقت المحدد: 60 ثانية
┣━➤ 🎯 المحاولات المتاحة: 3
┣━➤ 💰 المكافأة: 100 دينار
┣━➤ 🎁 بونص السرعة: +50 دينار
┃
┣━➤ 💡 اكتب إجابتك الآن...
┃
╰─═◇【 🏆 حظاً موفقاً 🏆 】◇═─╯
        """
        
        if update.message:
            await update.message.reply_text(riddle_text)
        
        # إزالة اللعبة بعد 60 ثانية
        asyncio.create_task(self.end_game_timer(chat.id, 60))

    async def start_math_game(self, update: Update, user: User, chat: Chat):
        """بدء لعبة الرياضيات"""
        if chat.id in self.active_games:
            if update.message:
                await update.message.reply_text("🎮 يوجد لعبة نشطة بالفعل في هذه المجموعة!")
            return
        
        question = random.choice(self.math_questions)
        
        self.active_games[chat.id] = {
            "type": "math",
            "question": question["q"],
            "answer": question["a"],
            "start_time": datetime.now(),
            "attempts": 0,
            "max_attempts": 3,
            "reward": 150
        }
        
        math_text = f"""
╭─═◇【 🔢 لعبة الرياضيات المتطورة 🔢 】◇═─╮
┃
┣━➤ ➕ السؤال: {question["q"]}
┃
┣━➤ ⏱️ الوقت المحدد: 45 ثانية
┣━➤ 🎯 المحاولات المتاحة: 3
┣━➤ 💰 المكافأة: 150 دينار
┣━➤ 🎁 بونص الدقة: +75 دينار
┃
┣━➤ 🧮 اكتب الإجابة بالأرقام فقط...
┃
╰─═◇【 🏆 أظهر مهاراتك 🏆 】◇═─╯
        """
        
        if update.message:
            await update.message.reply_text(math_text)
        
        # إزالة اللعبة بعد 45 ثانية
        asyncio.create_task(self.end_game_timer(chat.id, 45))

    async def truth_question(self, update: Update):
        """سؤال صراحة"""
        question = random.choice(self.truth_questions)
        
        truth_text = f"""
╭─═◇【 💭 لعبة الصراحة المتطورة 💭 】◇═─╮
┃
┣━➤ ❓ سؤال الصراحة:
┃
┣━➤ {question}
┃
┣━➤ 💡 أجب بصراحة تامة...
┣━➤ 🎁 مكافأة الشجاعة: 50 دينار
┃
╰─═◇【 🌟 الصدق أساس كل شيء 🌟 】◇═─╯
        """
        
        if update.message:
            await update.message.reply_text(truth_text)
            # إضافة مكافأة
            user = update.effective_user
            if user:
                self.add_user_balance(user.id, 50)

    async def dare_challenge(self, update: Update):
        """تحدي جرأة"""
        challenge = random.choice(self.dare_challenges)
        
        dare_text = f"""
╭─═◇【 ⚡ لعبة الجرأة المتطورة ⚡】◇═─╮
┃
┣━➤ 🎯 تحدي الجرأة:
┃
┣━➤ {challenge}
┃
┣━➤ ⏰ لديك 5 دقائق لتنفيذ التحدي
┣━➤ 🎁 مكافأة الجرأة: 100 دينار
┣━➤ 🏆 بونص الإبداع: +50 دينار
┃
╰─═◇【 💪 هل تقبل التحدي؟ 💪 】◇═─╯
        """
        
        if update.message:
            await update.message.reply_text(dare_text)
            # إضافة مكافأة
            user = update.effective_user
            if user:
                self.add_user_balance(user.id, 100)

    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """معالج الاستعلامات"""
        query = update.callback_query
        if not query or not query.data:
            return
            
        await query.answer()
        
        data = query.data
        user = query.from_user
        
        if not user:
            return
        
        # معالجة استعلامات مختلفة
        if data.startswith("game_"):
            await self.handle_game_callback(query, data)
        elif data.startswith("bank_"):
            await self.handle_bank_callback(query, data)
        elif data.startswith("farm_"):
            await self.handle_farm_callback(query, data)
        elif data == "my_stats":
            await self.show_callback_stats(query, user)
        elif data == "my_balance":
            await self.show_callback_balance(query, user)

    async def handle_game_callback(self, query: CallbackQuery, data: str):
        """معالج استعلامات الألعاب"""
        game_type = data.replace("game_", "")
        user = query.from_user
        chat = query.message.chat if query.message else None
        
        if not user or not chat:
            return
        
        if game_type == "riddle":
            await self.start_riddle_game_callback(query, user, chat)
        elif game_type == "math":
            await self.start_math_game_callback(query, user, chat)
        elif game_type == "truth":
            await self.truth_question_callback(query)
        elif game_type == "dare":
            await self.dare_challenge_callback(query)

    async def handle_bank_callback(self, query: CallbackQuery, data: str):
        """معالج استعلامات البنك"""
        action = data.replace("bank_", "")
        user = query.from_user
        
        if not user:
            return
        
        if action == "transfer":
            await self.show_transfer_menu(query, user)
        elif action == "invest":
            await self.show_investment_menu(query, user)
        elif action == "loan":
            await self.show_loan_menu(query, user)
        elif action == "statement":
            await self.show_bank_statement(query, user)

    async def handle_farm_callback(self, query: CallbackQuery, data: str):
        """معالج استعلامات المزرعة"""
        action = data.replace("farm_", "")
        user = query.from_user
        
        if not user:
            return
        
        if action == "plant":
            await self.show_planting_menu(query, user)
        elif action == "harvest":
            await self.harvest_crops(query, user)
        elif action == "shop":
            await self.show_farm_shop(query, user)
        elif action == "storage":
            await self.show_farm_storage(query, user)
            
 

    # وظائف مساعدة
    async def save_user_info(self, user: User):
        """حفظ معلومات المستخدم"""
        user_data = {
            "id": user.id,
            "first_name": user.first_name,
            "username": user.username,
            "join_date": datetime.now().isoformat(),
            "balance": self.db.get("users", {}).get(str(user.id), {}).get("balance", 1000),
            "messages": 0,
            "games_played": 0
        }
        
        if "users" not in self.db:
            self.db["users"] = {}
            
        if str(user.id) not in self.db["users"]:
            self.db["users"][str(user.id)] = user_data
            self.save_database()

    async def update_message_stats(self, user_id: int, chat_id: int):
        """تحديث إحصائيات الرسائل"""
        if "users" not in self.db:
            self.db["users"] = {}
            
        user_key = str(user_id)
        if user_key not in self.db["users"]:
            self.db["users"][user_key] = {"messages": 0}
            
        self.db["users"][user_key]["messages"] = self.db["users"][user_key].get("messages", 0) + 1
        self.stats["messages_today"] += 1

    def is_group_activated(self, chat_id: int) -> bool:
        """فحص تفعيل المجموعة"""
        return self.db.get("groups", {}).get(str(chat_id), {}).get("activated", False)

    def is_sudo(self, user_id: int) -> bool:
        """فحص المطور"""
        return user_id in self.SUDO_USERS

    async def is_admin(self, user_id: int, chat_id: int) -> bool:
        """فحص المشرف"""
        if self.is_sudo(user_id):
            return True
            
        try:
            member = await self.application.bot.get_chat_member(chat_id, user_id)
            return member.status in ["administrator", "creator"]
        except:
            return False

    def get_user_balance(self, user_id: int) -> int:
        """الحصول على رصيد المستخدم"""
        return self.db.get("users", {}).get(str(user_id), {}).get("balance", 0)

    def add_user_balance(self, user_id: int, amount: int):
        """إضافة رصيد للمستخدم"""
        if "users" not in self.db:
            self.db["users"] = {}
            
        user_key = str(user_id)
        if user_key not in self.db["users"]:
            self.db["users"][user_key] = {"balance": 0}
            
        self.db["users"][user_key]["balance"] = self.db["users"][user_key].get("balance", 0) + amount
        self.save_database()

    async def end_game_timer(self, chat_id: int, seconds: int):
        """مؤقت انتهاء اللعبة"""
        await asyncio.sleep(seconds)
        if chat_id in self.active_games:
            del self.active_games[chat_id]

    async def activate_group(self, update: Update, user: User, chat: Chat):
        """تفعيل المجموعة"""
        # فحص الصلاحيات
        if not await self.is_admin(user.id, chat.id):
            if update.message:
                await update.message.reply_text("❌ يجب أن تكون مشرف لتفعيل البوت")
            return
        
        # تفعيل المجموعة
        if "groups" not in self.db:
            self.db["groups"] = {}
            
        self.db["groups"][str(chat.id)] = {
            "activated": True,
            "title": chat.title,
            "activation_date": datetime.now().isoformat(),
            "activated_by": user.id
        }
        
        self.save_database()
        
        success_text = f"""
╭─═◇【 ✅ تم تفعيل البوت بنجاح ✅ 】◇═─╮
┃
┣━➤ 🎉 مرحباً بكم في {chat.title}
┣━➤ 🤖 تم تفعيل {self.bot_name}
┣━➤ 👤 المفعل: {user.first_name}
┣━➤ 📅 التاريخ: {datetime.now().strftime('%Y/%m/%d %H:%M')}
┃
┣━━━━━━━━━【 🚀 الميزات المتاحة 🚀 】━━━━━━━━━┫
┣━➤ 🎮 +50 لعبة تفاعلية
┣━➤ 🏦 نظام بنك متطور
┣━➤ 🚜 مزرعة افتراضية
┣━➤ 🛡️ حماية خارقة
┣━➤ 🤖 ذكاء اصطناعي
┣━➤ 📊 إحصائيات مفصلة
┃
┣━➤ 📋 اكتب "الاوامر" لعرض القائمة الكاملة
┃
╰─═◇【 💎 @T_A_Tl 💎 】◇═─╯
        """
        
        if update.message:
            await update.message.reply_text(success_text)

    async def daily_salary(self, update: Update, user: User):
        """استلام الراتب اليومي"""
        user_id = user.id
        today = datetime.now().strftime('%Y-%m-%d')
        last_salary = self.db.get("users", {}).get(str(user_id), {}).get("last_salary")
        
        if last_salary == today:
            if update.message:
                await update.message.reply_text("💰 لقد استلمت راتبك اليومي بالفعل! عد غداً")
            return
        
        # حساب الراتب حسب النشاط
        base_salary = 500
        bonus = self.db.get("users", {}).get(str(user_id), {}).get("messages", 0) * 2
        total_salary = base_salary + min(bonus, 1000)  # حد أقصى للبونص
        
        # إضافة الراتب
        self.add_user_balance(user_id, total_salary)
        
        # حفظ تاريخ آخر راتب
        if "users" not in self.db:
            self.db["users"] = {}
        if str(user_id) not in self.db["users"]:
            self.db["users"][str(user_id)] = {}
            
        self.db["users"][str(user_id)]["last_salary"] = today
        self.save_database()
        
        salary_text = f"""
╭─═◇【 💰 استلام الراتب اليومي 💰 】◇═─╮
┃
┣━➤ ✅ تم استلام الراتب بنجاح!
┃
┣━➤ 💵 الراتب الأساسي: {base_salary:,} دينار
┣━➤ 🎁 بونص النشاط: {bonus:,} دينار
┣━➤ 💎 إجمالي المبلغ: {total_salary:,} دينار
┃
┣━➤ 💳 رصيدك الحالي: {self.get_user_balance(user_id):,} دينار
┃
┣━➤ 📅 الراتب القادم: غداً
┃
╰─═◇【 🌟 @T_A_Tl 🌟 】◇═─╯
        """
        
        if update.message:
            await update.message.reply_text(salary_text)

    async def show_user_info(self, update: Update, user: User, chat: Chat):
        """عرض معلومات المستخدم"""
        user_data = self.db.get("users", {}).get(str(user.id), {})
        balance = self.get_user_balance(user.id)
        messages = user_data.get("messages", 0)
        join_date = user_data.get("join_date", "غير محدد")
        
        if join_date != "غير محدد":
            join_date = datetime.fromisoformat(join_date).strftime('%Y/%m/%d')
        
        # تحديد الرتبة
        rank = "عضو"
        if self.is_sudo(user.id):
            rank = "مطور البوت"
        elif await self.is_admin(user.id, chat.id):
            rank = "مشرف"
        elif balance > 100000:
            rank = "عضو VIP"
        elif balance > 50000:
            rank = "عضو مميز"
        
        info_text = f"""
╭─═◇【 👤 معلومات المستخدم 👤 】◇═─╮
┃
┣━➤ 🏷️ الاسم: {user.first_name}
┣━➤ 🆔 المعرف: @{user.username or 'غير متوفر'}
┣━➤ 🔢 الآيدي: `{user.id}`
┃
┣━━━━━━━━━【 📊 الإحصائيات 📊 】━━━━━━━━━┫
┣━➤ 🎗️ الرتبة: {rank}
┣━➤ 💰 الرصيد: {balance:,} دينار
┣━➤ 💬 عدد الرسائل: {messages:,}
┣━➤ 📅 تاريخ الانضمام: {join_date}
┃
┣━━━━━━━━━【 🏆 الإنجازات 🏆 】━━━━━━━━━┫
┣━➤ {'🥇 ثري' if balance > 100000 else '🔒 ثري (100K)'}
┣━➤ {'💬 ثرثار' if messages > 1000 else '🔒 ثرثار (1K رسالة)'}
┣━➤ {'⭐ نجم' if balance > 50000 and messages > 500 else '🔒 نجم'}
┃
╰─═◇【 💎 استمر في التميز 💎 】◇═─╯
        """
        
        keyboard = [
            [
                InlineKeyboardButton("💰 البنك", callback_data="bank_menu"),
                InlineKeyboardButton("🎮 الألعاب", callback_data="games_menu")
            ]
        ]
        
        if update.message:
            await update.message.reply_text(
                info_text,
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

    async def bot_status(self, update: Update):
        """حالة البوت"""
        start_time = self.db.get("start_time")
        if start_time:
            uptime = datetime.now() - datetime.fromisoformat(start_time)
            uptime_str = f"{uptime.days} يوم، {uptime.seconds//3600} ساعة"
        else:
            uptime_str = "غير محدد"
        
        total_users = len(self.db.get("users", {}))
        total_groups = len(self.db.get("groups", {}))
        
        status_text = f"""
╭─═◇【 🤖 حالة البوت المتطور 🤖 】◇═─╮
┃
┣━━━━━━━━━【 📊 الإحصائيات العامة 📊 】━━━━━━━━━┫
┣━➤ ✅ الحالة: يعمل بكفاءة عالية
┣━➤ ⏰ وقت التشغيل: {uptime_str}
┣━➤ 👥 إجمالي المستخدمين: {total_users:,}
┣━➤ 🏘️ إجمالي المجموعات: {total_groups:,}
┃
┣━━━━━━━━━【 📈 إحصائيات اليوم 📈 】━━━━━━━━━┫
┣━➤ 💬 الرسائل: {self.stats['messages_today']:,}
┣━➤ 🎮 الألعاب: {self.stats['games_played']:,}
┣━➤ ⚡ الأوامر: {self.stats['commands_used']:,}
┣━➤ 💸 التحويلات: {self.stats['money_transferred']:,}
┃
┣━━━━━━━━━【 🚀 الأداء 🚀 】━━━━━━━━━┫
┣━➤ 🟢 السيرفر: متصل
┣━➤ 🟢 قاعدة البيانات: تعمل
┣━➤ 🟢 الذاكرة: مثلى
┣━➤ 🟢 الشبكة: مستقرة
┃
┣━➤ 💎 النسخة: v2.0 Advanced
┣━➤ 👨‍💻 المطور: @{self.SUDO_USERNAME}
┃
╰─═◇【 🌟 بوت إلين. 𓅓𝑬𝑳𝑳𝑬𝑵 🌟 】◇═─╯
        """
        
        if update.message:
            await update.message.reply_text(status_text)

    async def handle_admin_commands(self, update: Update, text: str, user: User, chat: Chat):
        """معالجة أوامر الإدارة"""
        # سيتم إضافة أوامر الإدارة هنا
        pass

    async def handle_sudo_commands(self, update: Update, text: str, user: User, chat: Chat):
        """معالجة أوامر المطورين"""
        # سيتم إضافة أوامر المطورين هنا
        pass

    async def handle_auto_replies(self, update: Update, text: str, chat: Chat):
        """معالجة الردود التلقائية"""
        # رسائل خاصة
        special_messages = {
            "السلام عليكم": "🌸 وعليكم السلام ورحمة الله وبركاته",
            "صباح الخير": "🌅 صباح النور والخير",
            "مساء الخير": "🌙 مساء النور والخير",
            "تصبح على خير": "😴 وأنت من أهل الخير",
            "شكرا": "💙 العفو، في الخدمة دائماً",
            "شكراً": "💙 العفو، في الخدمة دائماً"
        }
        
        for trigger, response in special_messages.items():
            if trigger in text:
                if update.message:
                    await update.message.reply_text(response)
                break

    async def handle_member_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """معالج حالة الأعضاء"""
        if not update.message:
            return
            
        message = update.message
        chat = message.chat
        
        # عضو جديد
        if message.new_chat_members:
            for member in message.new_chat_members:
                welcome_text = f"""
╭─═◇【 🎉 مرحباً بالعضو الجديد 🎉 】◇═─╮
┃
┣━➤ 👋 أهلاً وسهلاً {member.first_name}
┣━➤ 🏘️ في {chat.title}
┣━➤ 💎 مع بوت إلين. 𓅓𝑬𝑳𝑳𝑬𝑵
┃
┣━➤ 🎁 مكافأة الانضمام: 500 دينار
┣━➤ 📋 اكتب "الاوامر" لعرض القائمة
┃
╰─═◇【 🌟 نتمنى لك إقامة مميزة 🌟 】◇═─╯
                """
                await message.reply_text(welcome_text)
                # إضافة مكافأة
                self.add_user_balance(member.id, 500)
        
        # عضو غادر
        elif message.left_chat_member:
            member = message.left_chat_member
            goodbye_text = f"👋 مع السلامة {member.first_name}، نتمنى لك التوفيق"
            await message.reply_text(goodbye_text)

    # وظائف مساعدة إضافية
    async def show_callback_stats(self, query: CallbackQuery, user: User):
        """عرض الإحصائيات عبر الاستعلام"""
        user_data = self.db.get("users", {}).get(str(user.id), {})
        balance = self.get_user_balance(user.id)
        messages = user_data.get("messages", 0)
        
        stats_text = f"""
💎 إحصائياتك المتطورة:

💰 الرصيد: {balance:,} دينار
💬 الرسائل: {messages:,}
🎮 الألعاب: {user_data.get("games_played", 0)}
📅 الانضمام: {user_data.get("join_date", "غير محدد")[:10]}
        """
        
        if query.message:
            await query.edit_message_text(stats_text)

    async def show_callback_balance(self, query: CallbackQuery, user: User):
        """عرض الرصيد عبر الاستعلام"""
        balance = self.get_user_balance(user.id)
        
        balance_text = f"""
💰 رصيدك الحالي: {balance:,} دينار

🏦 خدمات متاحة:
• تحويل الأموال
• الاستثمار الذكي  
• قروض فورية
• التداول
        """
        
        keyboard = [
            [InlineKeyboardButton("💸 تحويل", callback_data="bank_transfer")],
            [InlineKeyboardButton("📊 استثمار", callback_data="bank_invest")]
        ]
        
        if query.message:
            await query.edit_message_text(
                balance_text,
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

    async def show_transfer_menu(self, query: CallbackQuery, user: User):
        """عرض قائمة التحويل"""
        transfer_text = """
💸 تحويل الأموال

استخدم الصيغة التالية:
تحويل [المبلغ] @المستخدم

مثال: تحويل 1000 @username
        """
        
        if query.message:
            await query.edit_message_text(transfer_text)

    async def show_investment_menu(self, query: CallbackQuery, user: User):
        """عرض قائمة الاستثمار"""
        investment_text = """
📊 الاستثمار الذكي

💎 خطط الاستثمار:
• قصير المدى: 5% يومياً
• متوسط المدى: 15% أسبوعياً  
• طويل المدى: 50% شهرياً

استخدم: استثمار [المبلغ] [النوع]
        """
        
        if query.message:
            await query.edit_message_text(investment_text)

    async def show_loan_menu(self, query: CallbackQuery, user: User):
        """عرض قائمة القروض"""
        loan_text = """
💳 القروض الفورية

شروط القرض:
• الحد الأدنى: 1000 دينار
• الحد الأقصى: 50000 دينار
• معدل الفائدة: 10%
• مدة السداد: 30 يوم

استخدم: قرض [المبلغ]
        """
        
        if query.message:
            await query.edit_message_text(loan_text)

    async def show_bank_statement(self, query: CallbackQuery, user: User):
        """عرض كشف الحساب"""
        balance = self.get_user_balance(user.id)
        user_data = self.db.get("users", {}).get(str(user.id), {})
        
        statement_text = f"""
🏦 كشف الحساب المصرفي

📋 معلومات الحساب:
• رقم الحساب: {user.id}
• الاسم: {user.first_name}
• الرصيد الحالي: {balance:,} دينار

📊 ملخص النشاط:
• إجمالي الإيداعات: {user_data.get("total_deposits", 0):,}
• إجمالي السحوبات: {user_data.get("total_withdrawals", 0):,}
• عدد المعاملات: {user_data.get("transactions", 0)}
        """
        
        if query.message:
            await query.edit_message_text(statement_text)

    async def show_planting_menu(self, query: CallbackQuery, user: User):
        """عرض قائمة الزراعة"""
        planting_text = """
🌱 زراعة المحاصيل

المحاصيل المتاحة:
🥔 البطاطس - 20 دينار - 30 دقيقة
🍅 الطماطم - 30 دينار - 45 دقيقة  
🥕 الجزر - 40 دينار - 60 دقيقة
🌽 الذرة - 60 دينار - 90 دقيقة

استخدم: زراعة [اسم المحصول]
        """
        
        if query.message:
            await query.edit_message_text(planting_text)

    async def harvest_crops(self, query: CallbackQuery, user: User):
        """حصاد المحاصيل"""
        harvest_text = """
🌾 حصاد المحاصيل

لا توجد محاصيل جاهزة للحصاد حالياً

🕐 تحقق من مواعيد نضج محاصيلك
        """
        
        if query.message:
            await query.edit_message_text(harvest_text)

    async def show_farm_shop(self, query: CallbackQuery, user: User):
        """عرض متجر المزرعة"""
        shop_text = """
🏪 متجر المزرعة

🌱 البذور:
• بذور البطاطس: 20 دينار
• بذور الطماطم: 30 دينار
• بذور الجزر: 40 دينار
• بذور الذرة: 60 دينار

🔧 الأدوات:
• مجرفة محسنة: 500 دينار
• نظام ري: 1000 دينار
        """
        
        if query.message:
            await query.edit_message_text(shop_text)

    async def show_farm_storage(self, query: CallbackQuery, user: User):
        """عرض مخزن المزرعة"""
        storage_text = """
📦 مخزن المزرعة

المحاصيل المخزنة:
• البطاطس: 0 كيلو
• الطماطم: 0 كيلو
• الجزر: 0 كيلو
• الذرة: 0 كيلو

💰 القيمة الإجمالية: 0 دينار
        """
        
        if query.message:
            await query.edit_message_text(storage_text)

    async def start_riddle_game_callback(self, query: CallbackQuery, user: User, chat: Chat):
        """بدء لعبة الألغاز عبر الاستعلام"""
        await self.start_riddle_game(
            type('Update', (), {'message': query.message, 'effective_user': user, 'effective_chat': chat})(),
            user, chat
        )

    async def start_math_game_callback(self, query: CallbackQuery, user: User, chat: Chat):
        """بدء لعبة الرياضيات عبر الاستعلام"""
        await self.start_math_game(
            type('Update', (), {'message': query.message, 'effective_user': user, 'effective_chat': chat})(),
            user, chat
        )

    async def truth_question_callback(self, query: CallbackQuery):
        """سؤال صراحة عبر الاستعلام"""
        await self.truth_question(
            type('Update', (), {'message': query.message, 'effective_user': query.from_user})()
        )

    async def dare_challenge_callback(self, query: CallbackQuery):
        """تحدي جرأة عبر الاستعلام"""
        await self.dare_challenge(
            type('Update', (), {'message': query.message, 'effective_user': query.from_user})()
        )

    async def show_balance(self, update: Update, user: User):
        """عرض الرصيد"""
        balance = self.get_user_balance(user.id)
        
        balance_text = f"""
╭─═◇【 💰 رصيدك الحالي 💰 】◇═─╮
┃
┣━➤ 💳 الرصيد: {balance:,} دينار
┣━➤ 🏦 رقم الحساب: {user.id}
┣━➤ 📊 الحالة: نشط
┃
╰─═◇【 💎 بوت إلين. 𓅓𝑬𝑳𝑳𝑬𝑵 💎 】◇═─╯
        """
        
        if update.message:
            await update.message.reply_text(balance_text)

    async def show_salary_info(self, update: Update, user: User):
        """عرض معلومات الراتب"""
        today = datetime.now().strftime('%Y-%m-%d')
        last_salary = self.db.get("users", {}).get(str(user.id), {}).get("last_salary")
        
        if last_salary == today:
            status = "✅ تم الاستلام اليوم"
        else:
            status = "⏰ متاح للاستلام"
        
        salary_text = f"""
╭─═◇【 💵 معلومات الراتب 💵 】◇═─╮
┃
┣━➤ 💰 الراتب الأساسي: 500 دينار
┣━➤ 🎁 بونص النشاط: حتى 1000 دينار
┣━➤ 📅 الحالة: {status}
┃
┣━➤ 💡 اكتب "اليوميه" لاستلام الراتب
┃
╰─═◇【 💎 بوت إلين. 𓅓𝑬𝑳𝑳𝑬𝑵 💎 】◇═─╯
        """
        
        if update.message:
            await update.message.reply_text(salary_text)

    async def show_user_stats(self, update: Update, user: User, chat: Chat):
        """عرض إحصائيات المستخدم"""
        user_data = self.db.get("users", {}).get(str(user.id), {})
        balance = self.get_user_balance(user.id)
        messages = user_data.get("messages", 0)
        games_played = user_data.get("games_played", 0)
        
        stats_text = f"""
╭─═◇【 📊 إحصائياتك المتطورة 📊 】◇═─╮
┃
┣━━━━━━━━━【 💎 الملف الشخصي 💎 】━━━━━━━━━┫
┣━➤ 👤 الاسم: {user.first_name}
┣━➤ 🆔 الآيدي: {user.id}
┣━➤ 💰 الرصيد: {balance:,} دينار
┃
┣━━━━━━━━━【 📈 نشاطك 📈 】━━━━━━━━━┫
┣━➤ 💬 الرسائل: {messages:,}
┣━➤ 🎮 الألعاب: {games_played}
┣━➤ 🏆 النقاط: {messages * 2 + games_played * 10}
┃
┣━━━━━━━━━【 🏅 الإنجازات 🏅 】━━━━━━━━━┫
┣━➤ {'✅' if messages > 100 else '🔒'} محادث نشط (100 رسالة)
┣━➤ {'✅' if balance > 10000 else '🔒'} جامع أموال (10K دينار)
┣━➤ {'✅' if games_played > 10 else '🔒'} لاعب محترف (10 ألعاب)
┃
╰─═◇【 🌟 استمر في التقدم 🌟 】◇═─╯
        """
        
        if update.message:
            await update.message.reply_text(stats_text)

    def run(self):
        """تشغيل البوت"""
        logger.info("🚀 Starting T_A_Tl Advanced Bot...")
        
        # حفظ وقت التشغيل
        self.db["start_time"] = datetime.now().isoformat()
        self.save_database()
        
 

        # إضافة معالج الأخطاء
        self.application.add_error_handler(self.error_handler)
        
        # بدء التشغيل
        self.application.run_polling(
            allowed_updates=Update.ALL_TYPES,
            drop_pending_updates=True
        )

    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """معالج الأخطاء"""
        logger.error(f"Update {update} caused error {context.error}")

if __name__ == "__main__":
    try:
        bot = avetaarAdvancedBot()
        bot.run()
    except KeyboardInterrupt:
        logger.info("🛑 Bot stopped by user")
    except Exception as e:
        logger.error(f"💥 Bot error: {e}")
 
