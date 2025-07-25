
import { GoogleGenAI } from "@google/genai";

document.addEventListener('DOMContentLoaded', () => {

    // --- TYPE DEFINITIONS ---
    interface PlayerData { level: number; xp: number; }
    interface CoreStat { id: string; name: string; value: number; description: string; xp: number; }
    interface SecondaryAttribute { id: string; name: string; description: string; level: number; currentPoints: number; pointsForNextLevel: number; }
    interface Skill { id: string; name: string; description: string; level: number; currentPoints: number; pointsForNextLevel: number; }
    interface Achievement { id: string; text: string; }
    interface BentoItem { id: string; label: string; value: string; }
    interface UserProfile { description: string; philosophy: string; }
    interface Task { 
        id: string; 
        name: string; 
        playerXp: number; 
        attributeRewards: { attributeId: string; points: number; }[]; 
        coreStatXpRewards: { statId: string; xp: number; }[]; 
        skillRewards: { skillId: string; points: number; }[];
        completed: boolean; 
        punishment?: { xpLoss: number; };
    }
    interface ChecklistItem { id: string; text: string; completed: boolean; }
    interface CalendarDayData { note: string; checklist: ChecklistItem[]; }
    
    type StatLike = SecondaryAttribute | Skill;
    type StatLikeType = 'secondary-attribute' | 'skill';


    // --- STATE ---
    let currentDate = new Date();
    let calendarData: { [key: string]: CalendarDayData };
    let selectedDateKey: string | null = null;
    let selectedDayElement: HTMLElement | null = null;
    
    // Game state
    let playerData: PlayerData;
    let coreStats: CoreStat[];
    let secondaryAttributes: SecondaryAttribute[];
    let skills: Skill[];
    let userProfile: UserProfile;
    let achievements: Achievement[];
    let bentoData: BentoItem[];
    let dailyTasks: Task[];
    let weeklyTasks: Task[];
    let quests: Task[];
    let lastDailyReset: number;
    let lastWeeklyReset: number;
    let longPressTimer: number | undefined;
    
    // --- DOM ELEMENTS ---
    const pages = document.querySelectorAll<HTMLElement>('.page');
    const navButtons = document.querySelectorAll<HTMLButtonElement>('.nav-btn');
    
    // Calendar
    const calendarGrid = document.getElementById('calendar-grid');
    const monthYearHeader = document.getElementById('month-year');
    const prevMonthButton = document.getElementById('prev-month');
    const nextMonthButton = document.getElementById('next-month');
    const calendarDataModal = document.getElementById('calendar-data-modal');
    const calendarModalTitle = document.getElementById('calendar-modal-title');
    const calendarNoteInput = document.getElementById('calendar-note-input') as HTMLTextAreaElement;
    const calendarChecklist = document.getElementById('calendar-checklist');
    const addChecklistItemInput = document.getElementById('add-checklist-item-input') as HTMLInputElement;
    const addChecklistItemBtn = document.getElementById('add-checklist-item-btn');
    const saveCalendarDataButton = document.getElementById('save-calendar-data');
    const cancelCalendarDataButton = document.getElementById('cancel-calendar-data');
    const contextMenu = document.getElementById('context-menu');

    // Settings
    const settingsBtn = document.getElementById('settings-btn');
    const settingsModal = document.getElementById('settings-modal');
    const closeSettingsBtn = document.getElementById('close-settings');
    const darkModeToggle = document.getElementById('dark-mode-toggle') as HTMLInputElement;

    // Me Page
    const playerLevel = document.getElementById('player-level');
    const playerXp = document.getElementById('player-xp');
    const playerXpBar = document.getElementById('player-xp-bar');
    const radarChart = document.getElementById('radar-chart');
    const playerDescription = document.getElementById('player-description');
    const playerPhilosophy = document.getElementById('player-philosophy');
    const achievementsList = document.getElementById('achievements-list');
    const bentoGrid = document.getElementById('bento-grid');

    // Tasks Page
    const subNavButtons = document.querySelectorAll<HTMLButtonElement>('.sub-nav-btn');
    const taskListContainers = document.querySelectorAll('.task-list-container');
    const dailyTasksList = document.getElementById('daily-tasks-list');
    const weeklyTasksList = document.getElementById('weekly-tasks-list');
    const questsTasksList = document.getElementById('quests-tasks-list');
    const addTaskFab = document.getElementById('add-task-fab');

    // Stats & Skills Pages
    const coreStatsList = document.getElementById('core-stats-list');
    const secondaryAttributesList = document.getElementById('secondary-attributes-list');
    const skillsList = document.getElementById('skills-list');


    // Modals
    const formModal = document.getElementById('form-modal');
    const formModalTitle = document.getElementById('form-modal-title');
    const formModalBody = document.getElementById('form-modal-body');
    const formModalSave = document.getElementById('form-modal-save');
    const formModalCancel = document.getElementById('form-modal-cancel');
    const formModalDelete = document.getElementById('form-modal-delete');

    const confirmModal = document.getElementById('confirm-modal');
    const confirmModalTitle = document.getElementById('confirm-modal-title');
    const confirmModalBody = document.getElementById('confirm-modal-body');
    const confirmModalConfirm = document.getElementById('confirm-modal-confirm');
    const confirmModalCancel = document.getElementById('confirm-modal-cancel');


    // --- DATA MANAGEMENT ---

    const getXpForNextLevel = (level: number) => 1000 * Math.pow(2, level - 1);
    
    // --- IST Time Helpers & Default Data ---
    const IST_OFFSET = 5.5 * 60 * 60 * 1000;
    const getISTDate = (date = new Date()) => new Date(date.getTime() + IST_OFFSET);

    const getStartOfTodayIST = () => {
        const nowIst = getISTDate();
        return new Date(Date.UTC(nowIst.getUTCFullYear(), nowIst.getUTCMonth(), nowIst.getUTCDate())).getTime();
    };

    const getStartOfWeekIST = () => {
        const nowIst = getISTDate();
        const dayOfWeekIst = nowIst.getUTCDay(); // In UTC: Sunday is 0, Monday is 1...
        const daysToSubtract = (dayOfWeekIst + 6) % 7; // How many days to go back to get to Monday
        const startOfWeekDate = new Date(nowIst.getTime());
        startOfWeekDate.setUTCDate(startOfWeekDate.getUTCDate() - daysToSubtract);
        return new Date(Date.UTC(startOfWeekDate.getUTCFullYear(), startOfWeekDate.getUTCMonth(), startOfWeekDate.getUTCDate())).getTime();
    };

    const defaultData = {
        playerData: { level: 1, xp: 0 },
        coreStats: [
            { id: 'str', name: 'Strength', value: 10, description: 'Measures physical power, affecting heavy lifting, and physical damage.', xp: 0 },
            { id: 'dex', name: 'Dexterity', value: 10, description: 'Measures agility, reflexes, and balance, affecting coordination and speed.', xp: 0 },
            { id: 'con', name: 'Constitution', value: 10, description: 'Measures endurance, stamina, and health, affecting resilience and energy levels.', xp: 0 },
            { id: 'int', name: 'Intelligence', value: 10, description: 'Measures reasoning, memory, and analytical skill, affecting learning and problem-solving.', xp: 0 },
            { id: 'wis', name: 'Wisdom', value: 10, description: 'Measures perception, intuition, and insight, affecting decision-making and awareness.', xp: 0 },
            { id: 'cha', name: 'Charisma', value: 10, description: 'Measures force of personality, persuasiveness, and leadership, affecting social interactions.', xp: 0 },
        ],
        secondaryAttributes: [
            { id: 'disc', name: 'Discipline', description: 'Ability to stay focused and consistent.', level: 1, currentPoints: 0, pointsForNextLevel: 100 },
            { id: 'creat', name: 'Creativity', description: 'Ability to generate novel ideas.', level: 1, currentPoints: 0, pointsForNextLevel: 100 },
        ],
        skills: [],
        userProfile: { description: 'A brief description of yourself.', philosophy: 'Your core values and principles.' },
        achievements: [{id: '1', text: 'Started your journey!'}],
        bentoData: [{id: '1', label: 'Projects Done', value: '0'}],
        dailyTasks: [],
        weeklyTasks: [],
        quests: [],
        lastDailyReset: getStartOfTodayIST(),
        lastWeeklyReset: getStartOfWeekIST(),
        calendarData: '{}',
    };

    const loadData = () => {
        const mapTasks = (task: any): Task => ({
            ...task,
            attributeRewards: task.attributeRewards || [],
            coreStatXpRewards: task.coreStatXpRewards || [],
            skillRewards: task.skillRewards || [],
            punishment: task.punishment
        });

        playerData = JSON.parse(localStorage.getItem('playerData') || JSON.stringify(defaultData.playerData));
        const loadedCoreStats = JSON.parse(localStorage.getItem('coreStats') || JSON.stringify(defaultData.coreStats));
        coreStats = loadedCoreStats.map((stat: any) => ({ ...stat, xp: stat.xp ?? 0 }));
        secondaryAttributes = JSON.parse(localStorage.getItem('secondaryAttributes') || JSON.stringify(defaultData.secondaryAttributes));
        skills = JSON.parse(localStorage.getItem('skills') || JSON.stringify(defaultData.skills));
        userProfile = JSON.parse(localStorage.getItem('userProfile') || JSON.stringify(defaultData.userProfile));
        achievements = JSON.parse(localStorage.getItem('achievements') || JSON.stringify(defaultData.achievements));
        bentoData = JSON.parse(localStorage.getItem('bentoData') || JSON.stringify(defaultData.bentoData));
        dailyTasks = JSON.parse(localStorage.getItem('dailyTasks') || '[]').map(mapTasks);
        weeklyTasks = JSON.parse(localStorage.getItem('weeklyTasks') || '[]').map(mapTasks);
        quests = JSON.parse(localStorage.getItem('quests') || '[]').map(mapTasks);
        lastDailyReset = JSON.parse(localStorage.getItem('lastDailyReset') || JSON.stringify(defaultData.lastDailyReset));
        lastWeeklyReset = JSON.parse(localStorage.getItem('lastWeeklyReset') || JSON.stringify(defaultData.lastWeeklyReset));
        
        // Load and migrate calendar data
        const rawCalendarData = JSON.parse(localStorage.getItem('calendarData') || localStorage.getItem('calendarNotes') || defaultData.calendarData);
        calendarData = {};
        for(const key in rawCalendarData) {
            if(typeof rawCalendarData[key] === 'string'){
                calendarData[key] = { note: rawCalendarData[key], checklist: [] };
            } else {
                calendarData[key] = { note: rawCalendarData[key].note || '', checklist: rawCalendarData[key].checklist || [] };
            }
        }
        localStorage.removeItem('calendarNotes'); // remove old key
    };

    const saveData = () => {
        localStorage.setItem('playerData', JSON.stringify(playerData));
        localStorage.setItem('coreStats', JSON.stringify(coreStats));
        localStorage.setItem('secondaryAttributes', JSON.stringify(secondaryAttributes));
        localStorage.setItem('skills', JSON.stringify(skills));
        localStorage.setItem('userProfile', JSON.stringify(userProfile));
        localStorage.setItem('achievements', JSON.stringify(achievements));
        localStorage.setItem('bentoData', JSON.stringify(bentoData));
        localStorage.setItem('dailyTasks', JSON.stringify(dailyTasks));
        localStorage.setItem('weeklyTasks', JSON.stringify(weeklyTasks));
        localStorage.setItem('quests', JSON.stringify(quests));
        localStorage.setItem('lastDailyReset', JSON.stringify(lastDailyReset));
        localStorage.setItem('lastWeeklyReset', JSON.stringify(lastWeeklyReset));
        localStorage.setItem('calendarData', JSON.stringify(calendarData));
    };

    // --- TASK RESET LOGIC ---
    const handleTaskResets = () => {
        const startOfTodayIst = getStartOfTodayIST();

        // Daily reset check
        if (startOfTodayIst > lastDailyReset) {
            dailyTasks.forEach(task => {
                if (!task.completed && task.punishment && task.punishment.xpLoss > 0) {
                    addXp(-task.punishment.xpLoss);
                    quests.push({
                        id: Date.now().toString() + Math.random(),
                        name: `Punishment for not completing "${task.name}"`,
                        playerXp: 50,
                        attributeRewards: [],
                        coreStatXpRewards: [],
                        skillRewards: [],
                        completed: false
                    });
                }
            });
            dailyTasks.forEach(task => task.completed = false);
            lastDailyReset = startOfTodayIst;
        }

        // Weekly reset check
        const startOfWeekIst = getStartOfWeekIST();
        if (startOfWeekIst > lastWeeklyReset) {
            weeklyTasks.forEach(task => {
                if (!task.completed && task.punishment && task.punishment.xpLoss > 0) {
                    addXp(-task.punishment.xpLoss);
                    quests.push({
                        id: Date.now().toString() + Math.random(),
                        name: `Punishment for not completing "${task.name}"`,
                        playerXp: 100, // Higher reward for weekly punishment
                        attributeRewards: [],
                        coreStatXpRewards: [],
                        skillRewards: [],
                        completed: false
                    });
                }
            });
             weeklyTasks.forEach(task => task.completed = false);
             lastWeeklyReset = startOfWeekIst;
        }
    };


    // --- RENDERING FUNCTIONS ---
    
    // Me Page Rendering
    const renderXpBar = () => {
        if (!playerLevel || !playerXp || !playerXpBar) return;
        const xpNeeded = getXpForNextLevel(playerData.level);
        playerLevel.textContent = `Level ${playerData.level}`;
        playerXp.textContent = `${playerData.xp} / ${xpNeeded} XP`;
        const percentage = Math.min((playerData.xp / xpNeeded) * 100, 100);
        playerXpBar.style.width = `${percentage}%`;
    };

    const renderRadarChart = () => {
        if (!radarChart) return;
        const size = 300;
        const center = size / 2;
        const radius = center * 0.8;
        const numAxes = coreStats.length;
        if (numAxes < 3) {
            radarChart.innerHTML = `<text x="${center}" y="${center}" text-anchor="middle" fill="${getComputedStyle(document.body).getPropertyValue('--text-color')}">Need at least 3 core stats</text>`;
            return;
        }

        const angleSlice = (Math.PI * 2) / numAxes;
        
        let chartSvg = '';
        
        // Draw grid lines
        for (let i = 1; i <= 4; i++) {
            let points = '';
            for (let j = 0; j < numAxes; j++) {
                const angle = angleSlice * j - Math.PI / 2;
                const x = center + (radius * i / 4) * Math.cos(angle);
                const y = center + (radius * i / 4) * Math.sin(angle);
                points += `${x},${y} `;
            }
            chartSvg += `<polygon class="axis" points="${points.trim()}" fill="none" />`;
        }
        
        // Draw axes and labels
        coreStats.forEach((stat, i) => {
            const angle = angleSlice * i - Math.PI / 2;
            const x1 = center;
            const y1 = center;
            const x2 = center + radius * Math.cos(angle);
            const y2 = center + radius * Math.sin(angle);
            chartSvg += `<line class="axis" x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" />`;

            const labelX = center + (radius + 20) * Math.cos(angle);
            const labelY = center + (radius + 20) * Math.sin(angle);
            chartSvg += `<text class="label" x="${labelX}" y="${labelY}" text-anchor="middle" dominant-baseline="middle">${stat.name}</text>`;
        });

        // Draw data shape
        // Assuming stats range from 0 to 20 for scaling
        const maxValue = 20;
        let dataPoints = '';
        coreStats.forEach((stat, i) => {
            const valueRatio = Math.min(stat.value, maxValue) / maxValue;
            const angle = angleSlice * i - Math.PI / 2;
            const x = center + (radius * valueRatio) * Math.cos(angle);
            const y = center + (radius * valueRatio) * Math.sin(angle);
            dataPoints += `${x},${y} `;
        });
        chartSvg += `<polygon class="shape" points="${dataPoints.trim()}" />`;

        radarChart.innerHTML = chartSvg;
    };

    const renderProfile = () => {
        if (playerDescription) playerDescription.textContent = userProfile.description;
        if (playerPhilosophy) playerPhilosophy.textContent = userProfile.philosophy;
    };

    const renderAchievements = () => {
        if (!achievementsList) return;
        achievementsList.innerHTML = '';
        achievements.forEach(ach => {
            const li = document.createElement('li');
            li.textContent = ach.text;
            li.dataset.id = ach.id;
            li.addEventListener('click', () => showFormModal('achievement', ach));
            achievementsList.appendChild(li);
        });
    };
    
    const renderBentoGrid = () => {
        if (!bentoGrid) return;
        bentoGrid.innerHTML = '';
        bentoData.forEach(item => {
            const box = document.createElement('div');
            box.className = 'bento-box';
            box.dataset.id = item.id;
            box.innerHTML = `<div class="label">${item.label}</div><div class="value">${item.value}</div>`;
            box.addEventListener('click', () => showFormModal('bento', item));
            bentoGrid.appendChild(box);
        });
    };
    
    const renderMePage = () => {
        renderXpBar();
        renderRadarChart();
        renderProfile();
        renderAchievements();
        renderBentoGrid();
    };

    // Stats & Skills Page Rendering
    const renderCoreStats = () => {
        if (!coreStatsList) return;
        coreStatsList.innerHTML = '';
        coreStats.forEach(stat => {
            const item = document.createElement('div');
            item.className = 'stat-item';
            const xpPercentage = stat.xp >= 0 
                ? Math.min((stat.xp / 100) * 100, 100)
                : Math.min((Math.abs(stat.xp) / 50) * 100, 100);
            const xpBarClass = stat.xp >= 0 ? 'positive-xp' : 'negative-xp';

            item.innerHTML = `
                <div class="stat-item-header">
                    <span class="stat-item-name">${stat.name}</span>
                    <span class="stat-item-value">${stat.value}</span>
                </div>
                <div class="stat-item-details">
                    <p class="stat-description">${stat.description}</p>
                    <div class="core-stat-xp-info">
                        <span>XP: ${stat.xp} / ${stat.xp >= 0 ? 100 : -50}</span>
                    </div>
                    <div class="progress-bar-container core-stat-xp-bar-container">
                        <div class="progress-bar core-stat-xp-bar ${xpBarClass}" style="width: ${xpPercentage}%;"></div>
                    </div>
                    <div class="stat-item-actions">
                        <button class="edit-btn">Edit</button>
                    </div>
                </div>
            `;
            item.querySelector('.stat-item-header')?.addEventListener('click', () => item.classList.toggle('open'));
            item.querySelector('.edit-btn')?.addEventListener('click', (e) => {
                e.stopPropagation();
                showFormModal('core-stat', stat);
            });
            coreStatsList.appendChild(item);
        });
    };

    const renderStatLikeList = (listElement: HTMLElement | null, items: StatLike[], type: StatLikeType) => {
        if (!listElement) return;
        listElement.innerHTML = '';
        items.forEach(item => {
            const el = document.createElement('div');
            el.className = 'stat-item';
            const progress = (item.currentPoints / item.pointsForNextLevel) * 100;
            el.innerHTML = `
                <div class="stat-item-header">
                    <span class="stat-item-name">${item.name}<span class="stat-item-level">Lvl ${item.level}</span></span>
                </div>
                <div class="stat-item-details">
                    <p class="stat-description">${item.description}</p>
                    <div class="stat-progress-info">
                        <span>${item.currentPoints} / ${item.pointsForNextLevel}</span>
                        <span>Next Level</span>
                    </div>
                    <div class="progress-bar-container">
                        <div class="progress-bar" style="width: ${progress}%;"></div>
                    </div>
                    <div class="stat-item-actions">
                        <button class="edit-btn">Edit</button>
                    </div>
                </div>
            `;
            el.querySelector('.stat-item-header')?.addEventListener('click', () => el.classList.toggle('open'));
            el.querySelector('.edit-btn')?.addEventListener('click', (e) => {
                e.stopPropagation();
                showFormModal(type, item);
            });
            listElement.appendChild(el);
        });
    };
    
    const renderStatsPage = () => {
        renderCoreStats();
        renderStatLikeList(secondaryAttributesList, secondaryAttributes, 'secondary-attribute');
    };

    const renderSkillsPage = () => {
        renderStatLikeList(skillsList, skills, 'skill');
    };

    // Tasks Page Rendering
    const renderTasks = (listElement: HTMLElement | null, tasks: Task[], type: 'daily' | 'weekly' | 'quest') => {
        if (!listElement) return;
        listElement.innerHTML = '';
        if (tasks.length === 0) {
            listElement.innerHTML = `<li class="no-tasks-message">No ${type} tasks yet.</li>`;
        }
        tasks.forEach(task => {
            const li = document.createElement('li');
            li.className = `task-item ${task.completed ? 'completed' : ''}`;
            
            const rewardsHtml = [`<span class="xp-reward">+${task.playerXp} XP</span>`];
            if (task.punishment && task.punishment.xpLoss > 0) {
                rewardsHtml.push(`<span class="punishment-indicator" title="Failure penalty: ${task.punishment.xpLoss} XP">!</span>`);
            }

            task.coreStatXpRewards.forEach(reward => {
                const stat = coreStats.find(s => s.id === reward.statId);
                if (stat) {
                    rewardsHtml.push(`<span class="core-stat-reward">+${reward.xp} ${stat.name} XP</span>`);
                }
            });
            task.attributeRewards.forEach(reward => {
                const attr = secondaryAttributes.find(a => a.id === reward.attributeId);
                if (attr) {
                    rewardsHtml.push(`<span class="attr-reward">+${reward.points} ${attr.name}</span>`);
                }
            });
            task.skillRewards.forEach(reward => {
                const skill = skills.find(s => s.id === reward.skillId);
                if (skill) {
                    rewardsHtml.push(`<span class="skill-reward">+${reward.points} ${skill.name} XP</span>`);
                }
            });

            let completionControlHtml = '';
            if (type === 'daily' || type === 'weekly') {
                completionControlHtml = `
                    <button class="complete-task-btn" data-id="${task.id}" data-type="${type}" ${task.completed ? 'disabled' : ''} aria-label="Complete task: ${task.name}">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
                    </button>
                `;
            } else { // 'quest'
                completionControlHtml = `<input type="checkbox" class="task-checkbox" ${task.completed ? 'checked' : ''} data-id="${task.id}" data-type="${type}">`;
            }

            li.innerHTML = `
                ${completionControlHtml}
                <div class="task-details">
                    <div class="task-name">${task.name}</div>
                    <div class="task-rewards">${rewardsHtml.join('')}</div>
                </div>
                <button class="edit-task-btn" data-id="${task.id}" data-type="${type}">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg>
                </button>
            `;
            listElement.appendChild(li);
        });
        
        listElement.querySelectorAll('.task-checkbox').forEach(checkbox => {
            checkbox.addEventListener('change', handleTaskCompletion);
        });
        listElement.querySelectorAll('.complete-task-btn').forEach(button => {
            button.addEventListener('click', handleTaskCompletion);
        });
        listElement.querySelectorAll('.edit-task-btn').forEach(button => {
            button.addEventListener('click', handleEditTask);
        });
    };
    
    const renderTasksPage = () => {
        renderTasks(dailyTasksList, dailyTasks, 'daily');
        renderTasks(weeklyTasksList, weeklyTasks, 'weekly');
        renderTasks(questsTasksList, quests, 'quest');
    };
    
    // --- CORE GAME LOGIC ---

    const addXp = (amount: number) => {
        playerData.xp += amount;
        let xpNeeded = getXpForNextLevel(playerData.level);
        while (playerData.xp >= xpNeeded) {
            playerData.level++;
            playerData.xp -= xpNeeded;
            // TODO: Add a nice level up notification
            console.log(`Leveled up to ${playerData.level}!`);
            xpNeeded = getXpForNextLevel(playerData.level);
        }
    };

    const addCoreStatXp = (statId: string, amount: number) => {
        const stat = coreStats.find(s => s.id === statId);
        if (!stat) return;

        stat.xp += amount;
        
        while (stat.xp >= 100) {
            stat.value++;
            stat.xp -= 100;
            console.log(`${stat.name} increased to ${stat.value}!`);
        }

        while (stat.xp <= -50) {
            stat.value--;
            stat.xp += 50;
             console.log(`${stat.name} decreased to ${stat.value}!`);
        }
    };

    const addAttributePoints = (attributeId: string, points: number) => {
        const attr = secondaryAttributes.find(a => a.id === attributeId);
        if (!attr || attr.level >= 100) return;
        
        attr.currentPoints += points;
        while (attr.currentPoints >= attr.pointsForNextLevel) {
            attr.level++;
            attr.currentPoints -= attr.pointsForNextLevel;
            attr.pointsForNextLevel = Math.round(attr.pointsForNextLevel * 1.5); 
            console.log(`${attr.name} leveled up to ${attr.level}!`);
        }
    };

    const addSkillPoints = (skillId: string, points: number) => {
        const skill = skills.find(s => s.id === skillId);
        if (!skill || skill.level >= 100) return;

        skill.currentPoints += points;
        while (skill.currentPoints >= skill.pointsForNextLevel) {
            skill.level++;
            skill.currentPoints -= skill.pointsForNextLevel;
            skill.pointsForNextLevel = Math.round(skill.pointsForNextLevel * 1.5);
            console.log(`${skill.name} leveled up to ${skill.level}!`);
        }
    };

    const handleTaskCompletion = (e: Event) => {
        const target = e.currentTarget as HTMLElement;
        const taskId = target.dataset.id;
        const taskType = target.dataset.type as 'daily' | 'weekly' | 'quest';
        if (!taskId) return;

        const taskList = taskType === 'daily' ? dailyTasks : taskType === 'weekly' ? weeklyTasks : quests;
        const task = taskList.find(t => t.id === taskId);
        if (!task) return;
        
        // Prevent action if already completed
        if (task.completed) {
            if (target.tagName === 'INPUT') { // Prevent unchecking
                (target as HTMLInputElement).checked = true;
            }
            return;
        }

        showConfirmation(
            `Complete "${task.name}"?`, 
            `You will gain ${task.playerXp} XP and associated rewards.`, 
            () => {
                task.completed = true;
                addXp(task.playerXp);
                task.coreStatXpRewards.forEach(reward => {
                    addCoreStatXp(reward.statId, reward.xp);
                });
                task.attributeRewards.forEach(reward => {
                    addAttributePoints(reward.attributeId, reward.points);
                });
                task.skillRewards.forEach(reward => {
                    addSkillPoints(reward.skillId, reward.points);
                });
                
                saveData();
                renderAll();
            },
            () => {
                // Revert checkbox if user cancels
                if (target.tagName === 'INPUT') {
                    (target as HTMLInputElement).checked = false;
                }
            }
        );
    };

    const handleEditTask = (e: Event) => {
        const button = (e.target as HTMLElement).closest('button');
        if (!button) return;
        const taskId = button.dataset.id;
        const taskType = button.dataset.type as 'daily' | 'weekly' | 'quest';
        const taskList = taskType === 'daily' ? dailyTasks : taskType === 'weekly' ? weeklyTasks : quests;
        const task = taskList.find(t => t.id === taskId);
        if (task) {
            let formType: string;
            if (taskType === 'daily') formType = 'daily-task';
            else if (taskType === 'weekly') formType = 'weekly-task';
            else formType = 'quest-task';
            showFormModal(formType, task);
        }
    };


    // --- MODAL & FORM HANDLING ---
    
    const showConfirmation = (title: string, body: string, onConfirm: () => void, onCancel: () => void = () => {}) => {
        if (!confirmModal || !confirmModalTitle || !confirmModalBody || !confirmModalConfirm || !confirmModalCancel) return;
        
        confirmModalTitle.textContent = title;
        confirmModalBody.textContent = body;
        confirmModal.classList.remove('hidden');

        const confirmHandler = () => {
            onConfirm();
            hideConfirmation();
        };

        const cancelHandler = () => {
            onCancel();
            hideConfirmation();
        }
        
        const hideConfirmation = () => {
            confirmModal.classList.add('hidden');
            confirmModalConfirm.removeEventListener('click', confirmHandler);
            confirmModalCancel.removeEventListener('click', cancelHandler);
        };
        
        confirmModalConfirm.addEventListener('click', confirmHandler);
        confirmModalCancel.addEventListener('click', cancelHandler);
    };

    let formSubmitHandler: ((e: Event) => void) | null = null;
    let formDeleteHandler: ((e: Event) => void) | null = null;

    const showFormModal = (type: string, data: any = null) => {
        if (!formModal || !formModalTitle || !formModalBody || !formModalDelete) return;

        // Helper functions for creating reward rows
        const createAttrRewardRow = (reward: { attributeId: string; points: any } = { attributeId: '', points: '' }) => {
            const options = secondaryAttributes.map(attr => 
                `<option value="${attr.id}" ${attr.id === reward.attributeId ? 'selected' : ''}>${attr.name}</option>`
            ).join('');
            return `
                <div class="task-attribute-field">
                    <select class="attribute-select"><option value="">--Select Attribute--</option>${options}</select>
                    <input type="number" class="attribute-points" placeholder="Points" value="${reward.points || ''}">
                    <button type="button" class="remove-reward-btn" aria-label="Remove reward">&times;</button>
                </div>`;
        };
        const createCoreRewardRow = (reward: { statId: string; xp: any } = { statId: '', xp: '' }) => {
             const options = coreStats.map(stat => 
                `<option value="${stat.id}" ${stat.id === reward.statId ? 'selected' : ''}>${stat.name}</option>`
            ).join('');
             return `
                <div class="task-core-stat-field">
                    <select class="core-stat-select"><option value="">--Select Core Stat--</option>${options}</select>
                    <input type="number" class="core-stat-xp" placeholder="XP" value="${reward.xp || ''}">
                    <button type="button" class="remove-reward-btn" aria-label="Remove reward">&times;</button>
                </div>`;
        };
        const createSkillRewardRow = (reward: { skillId: string; points: any } = { skillId: '', points: '' }) => {
            const options = skills.map(skill => 
                `<option value="${skill.id}" ${skill.id === reward.skillId ? 'selected' : ''}>${skill.name}</option>`
            ).join('');
            return `
                <div class="task-skill-field">
                    <select class="skill-select"><option value="">--Select Skill--</option>${options}</select>
                    <input type="number" class="skill-points" placeholder="Points" value="${reward.points || ''}">
                    <button type="button" class="remove-reward-btn" aria-label="Remove reward">&times;</button>
                </div>`;
        };

        formModalDelete.classList.add('hidden');
        let formHtml = '';
        
        switch(type) {
            case 'core-stat':
                formModalTitle.textContent = data ? 'Edit Core Stat' : 'Add Core Stat';
                formModalDelete.classList.toggle('hidden', !data);
                formHtml = `
                    <div class="form-field"><label for="name">Name</label><input type="text" id="name" value="${data?.name || ''}"></div>
                    <div class="form-field"><label for="value">Value</label><input type="number" id="value" value="${data?.value || 10}"></div>
                    <div class="form-field"><label for="xp">XP</label><input type="number" id="xp" value="${data?.xp || 0}"></div>
                    <div class="form-field"><label for="description">Description</label><textarea id="description">${data?.description || ''}</textarea></div>
                `;
                break;
            case 'secondary-attribute':
            case 'skill':
                 const title = type === 'skill' ? 'Skill' : 'Secondary Attribute';
                 formModalTitle.textContent = data ? `Edit ${title}` : `Add ${title}`;
                 formModalDelete.classList.toggle('hidden', !data);
                 formHtml = `
                    <div class="form-field"><label for="name">Name</label><input type="text" id="name" value="${data?.name || ''}"></div>
                    <div class="form-field"><label for="description">Description</label><textarea id="description">${data?.description || ''}</textarea></div>
                    <div class="form-field"><label for="pointsForNextLevel">Points for Next Level</label><input type="number" id="pointsForNextLevel" value="${data?.pointsForNextLevel || 100}"></div>
                `;
                break;
             case 'daily-task':
             case 'weekly-task':
             case 'quest-task':
                 formModalTitle.textContent = data ? 'Edit Task' : 'Add Task';
                 formModalDelete.classList.toggle('hidden', !data);
                 
                const attrRewardsHtml = data?.attributeRewards?.map(createAttrRewardRow).join('') || '';
                const coreRewardsHtml = data?.coreStatXpRewards?.map(createCoreRewardRow).join('') || '';
                const skillRewardsHtml = data?.skillRewards?.map(createSkillRewardRow).join('') || '';

                const punishmentSection = (type === 'daily-task' || type === 'weekly-task') ? `
                    <div id="task-punishment-container">
                        <div class="task-punishment-field">
                            <input type="checkbox" id="add-punishment" ${data?.punishment ? 'checked' : ''}>
                            <label for="add-punishment">Add punishment for failure</label>
                        </div>
                        <div class="form-field punishment-details ${data?.punishment ? '' : 'hidden'}">
                            <label for="punishmentXpLoss">Player XP Loss</label>
                            <input type="number" id="punishmentXpLoss" value="${data?.punishment?.xpLoss || ''}" placeholder="e.g., 20">
                        </div>
                    </div>
                ` : '';

                 formHtml = `
                    <div class="form-field"><label for="name">Task Name</label><input type="text" id="name" value="${data?.name || ''}"></div>
                    <div class="form-field"><label for="playerXp">Player XP Reward</label><input type="number" id="playerXp" value="${data?.playerXp || 10}"></div>
                    
                    <div id="task-core-stats-container">
                        <label>Core Stat XP Rewards</label>
                        <div id="task-core-rewards-list">${coreRewardsHtml}</div>
                        <button type="button" id="add-core-reward-btn" class="add-btn-small">+ Add Core Stat Reward</button>
                    </div>

                    <div id="task-attributes-container">
                        <label>Attribute Rewards</label>
                        <div id="task-rewards-list">${attrRewardsHtml}</div>
                        <button type="button" id="add-reward-btn" class="add-btn-small">+ Add Attribute Reward</button>
                    </div>

                    <div id="task-skills-container">
                        <label>Skill XP Rewards</label>
                        <div id="task-skill-rewards-list">${skillRewardsHtml}</div>
                        <button type="button" id="add-skill-reward-btn" class="add-btn-small">+ Add Skill Reward</button>
                    </div>

                    ${punishmentSection}
                 `;
                break;
            case 'description':
            case 'philosophy':
                 formModalTitle.textContent = `Edit ${type.charAt(0).toUpperCase() + type.slice(1)}`;
                 formHtml = `<div class="form-field"><textarea id="text" rows="8">${data}</textarea></div>`;
                 break;
            case 'achievement':
                formModalTitle.textContent = data ? 'Edit Achievement' : 'Add Achievement';
                formModalDelete.classList.toggle('hidden', !data);
                formHtml = `<div class="form-field"><input type="text" id="text" value="${data?.text || ''}"></div>`;
                break;
            case 'bento':
                formModalTitle.textContent = data ? 'Edit Data Box' : 'Add Data Box';
                formModalDelete.classList.toggle('hidden', !data);
                formHtml = `
                    <div class="form-field"><label for="label">Label</label><input type="text" id="label" value="${data?.label || ''}"></div>
                    <div class="form-field"><label for="value">Value</label><input type="text" id="value" value="${data?.value || ''}"></div>
                `;
                break;
        }

        formModalBody.innerHTML = formHtml;
        formModal.classList.remove('hidden');
        
        // Add event listeners for dynamic reward rows in task forms
        if (type.endsWith('-task')) {
            formModalBody.querySelector('#add-reward-btn')?.addEventListener('click', () => {
                formModalBody.querySelector('#task-rewards-list')?.insertAdjacentHTML('beforeend', createAttrRewardRow());
            });
            formModalBody.querySelector('#task-rewards-list')?.addEventListener('click', (e) => {
                if ((e.target as HTMLElement).closest('.remove-reward-btn')) {
                    (e.target as HTMLElement).closest('.task-attribute-field')?.remove();
                }
            });

            formModalBody.querySelector('#add-core-reward-btn')?.addEventListener('click', () => {
                formModalBody.querySelector('#task-core-rewards-list')?.insertAdjacentHTML('beforeend', createCoreRewardRow());
            });
            formModalBody.querySelector('#task-core-rewards-list')?.addEventListener('click', (e) => {
                if ((e.target as HTMLElement).closest('.remove-reward-btn')) {
                    (e.target as HTMLElement).closest('.task-core-stat-field')?.remove();
                }
            });
            
            formModalBody.querySelector('#add-skill-reward-btn')?.addEventListener('click', () => {
                formModalBody.querySelector('#task-skill-rewards-list')?.insertAdjacentHTML('beforeend', createSkillRewardRow());
            });
            formModalBody.querySelector('#task-skill-rewards-list')?.addEventListener('click', (e) => {
                if ((e.target as HTMLElement).closest('.remove-reward-btn')) {
                    (e.target as HTMLElement).closest('.task-skill-field')?.remove();
                }
            });

            if (type === 'daily-task' || type === 'weekly-task') {
                const punishmentCheckbox = formModalBody.querySelector('#add-punishment');
                const punishmentDetails = formModalBody.querySelector('.punishment-details');
                punishmentCheckbox?.addEventListener('change', (e) => {
                    punishmentDetails?.classList.toggle('hidden', !(e.target as HTMLInputElement).checked);
                });
            }
        }

        // Clean up old handlers
        if (formSubmitHandler) formModalSave?.removeEventListener('click', formSubmitHandler);
        if (formDeleteHandler) formModalDelete?.removeEventListener('click', formDeleteHandler);
        
        // Add new handlers
        formSubmitHandler = () => handleFormSave(type, data?.id);
        formDeleteHandler = () => handleFormDelete(type, data?.id);
        formModalSave?.addEventListener('click', formSubmitHandler);
        if (data) {
           formModalDelete?.addEventListener('click', formDeleteHandler);
        }
    };
    
    const hideFormModal = () => {
        formModal?.classList.add('hidden');
        if (formSubmitHandler) formModalSave?.removeEventListener('click', formSubmitHandler);
        if (formDeleteHandler) formModalDelete?.removeEventListener('click', formDeleteHandler);
        formSubmitHandler = null;
        formDeleteHandler = null;
    };

    const handleFormSave = (type: string, id: string | null) => {
        const getFieldValue = (selector: string, isTextarea = false) => {
            const el = formModalBody?.querySelector(selector) as (HTMLInputElement | HTMLTextAreaElement);
            return el ? el.value : '';
        };
        const getFieldNumValue = (selector: string) => parseInt(getFieldValue(selector)) || 0;

        switch (type) {
            case 'core-stat': {
                const stat: CoreStat = { 
                    id: id || Date.now().toString(), 
                    name: getFieldValue('#name'), 
                    value: getFieldNumValue('#value'),
                    xp: getFieldNumValue('#xp'),
                    description: getFieldValue('#description', true) 
                };
                if (id) coreStats = coreStats.map(s => s.id === id ? stat : s);
                else coreStats.push(stat);
                break;
            }
            case 'secondary-attribute':
            case 'skill': {
                const isSkill = type === 'skill';
                const list: Array<StatLike> = isSkill ? skills : secondaryAttributes;
                const newItem: StatLike = { 
                    id: id || Date.now().toString(), 
                    name: getFieldValue('#name'), 
                    description: getFieldValue('#description', true), 
                    pointsForNextLevel: getFieldNumValue('#pointsForNextLevel') || 100, 
                    level: id ? list.find(s=>s.id===id)!.level : 1, 
                    currentPoints: id ? list.find(s=>s.id===id)!.currentPoints : 0 
                };
                if (id) {
                    if (isSkill) skills = skills.map(a => a.id === id ? newItem as Skill : a);
                    else secondaryAttributes = secondaryAttributes.map(a => a.id === id ? newItem as SecondaryAttribute : a);
                } else {
                     if (isSkill) skills.push(newItem as Skill);
                    else secondaryAttributes.push(newItem as SecondaryAttribute);
                }
                break;
            }
            case 'daily-task':
            case 'weekly-task':
            case 'quest-task': {
                 let taskList: Task[];
                 if (type === 'daily-task') taskList = dailyTasks;
                 else if (type === 'weekly-task') taskList = weeklyTasks;
                 else taskList = quests;

                 const attributeRewards: { attributeId: string; points: number }[] = [];
                 formModalBody.querySelectorAll('#task-rewards-list .task-attribute-field').forEach(field => {
                     const select = field.querySelector('.attribute-select') as HTMLSelectElement;
                     const input = field.querySelector('.attribute-points') as HTMLInputElement;
                     if(select.value && input.value){
                         attributeRewards.push({attributeId: select.value, points: parseInt(input.value) || 0});
                     }
                 });
                 
                 const coreStatXpRewards: { statId: string; xp: number }[] = [];
                 formModalBody.querySelectorAll('#task-core-rewards-list .task-core-stat-field').forEach(field => {
                     const select = field.querySelector('.core-stat-select') as HTMLSelectElement;
                     const input = field.querySelector('.core-stat-xp') as HTMLInputElement;
                     if(select.value && input.value){
                         coreStatXpRewards.push({statId: select.value, xp: parseInt(input.value) || 0});
                     }
                 });
                 
                 const skillRewards: { skillId: string; points: number }[] = [];
                 formModalBody.querySelectorAll('#task-skill-rewards-list .task-skill-field').forEach(field => {
                     const select = field.querySelector('.skill-select') as HTMLSelectElement;
                     const input = field.querySelector('.skill-points') as HTMLInputElement;
                     if(select.value && input.value){
                         skillRewards.push({skillId: select.value, points: parseInt(input.value) || 0});
                     }
                 });

                 let punishment: Task['punishment'] | undefined = undefined;
                 const addPunishmentCheckbox = formModalBody.querySelector('#add-punishment') as HTMLInputElement | null;
                 if (addPunishmentCheckbox?.checked) {
                     const xpLossInput = formModalBody.querySelector('#punishmentXpLoss') as HTMLInputElement;
                     const xpLoss = parseInt(xpLossInput?.value) || 0;
                     if (xpLoss > 0) {
                         punishment = { xpLoss };
                     }
                 }

                 const task: Task = { 
                    id: id || Date.now().toString(), 
                    name: getFieldValue('#name'), 
                    playerXp: getFieldNumValue('#playerXp'), 
                    attributeRewards, 
                    coreStatXpRewards,
                    skillRewards,
                    completed: id ? taskList.find(t=>t.id===id)!.completed : false,
                    punishment
                };
                 
                 if (id) {
                    const index = taskList.findIndex(t => t.id === id);
                    if (index !== -1) taskList[index] = task;
                 } else {
                    taskList.push(task);
                 }
                break;
            }
            case 'description': userProfile.description = getFieldValue('#text', true); break;
            case 'philosophy': userProfile.philosophy = getFieldValue('#text', true); break;
            case 'achievement': {
                const achievement = { id: id || Date.now().toString(), text: getFieldValue('#text') };
                if (id) achievements = achievements.map(a => a.id === id ? achievement : a);
                else achievements.push(achievement);
                break;
            }
            case 'bento': {
                const bento = { id: id || Date.now().toString(), label: getFieldValue('#label'), value: getFieldValue('#value') };
                if (id) bentoData = bentoData.map(b => b.id === id ? bento : b);
                else bentoData.push(bento);
                break;
            }
        }
        
        saveData();
        renderAll();
        hideFormModal();
    };

    const handleFormDelete = (type: string, id: string | null) => {
        if (!id) return;
        showConfirmation('Delete this item?', 'This action cannot be undone.', () => {
             switch (type) {
                case 'core-stat': coreStats = coreStats.filter(s => s.id !== id); break;
                case 'secondary-attribute': secondaryAttributes = secondaryAttributes.filter(a => a.id !== id); break;
                case 'skill': skills = skills.filter(s => s.id !== id); break;
                case 'daily-task': dailyTasks = dailyTasks.filter(t => t.id !== id); break;
                case 'weekly-task': weeklyTasks = weeklyTasks.filter(t => t.id !== id); break;
                case 'quest-task': quests = quests.filter(t => t.id !== id); break;
                case 'achievement': achievements = achievements.filter(a => a.id !== id); break;
                case 'bento': bentoData = bentoData.filter(b => b.id !== id); break;
             }
             saveData();
             renderAll();
             hideFormModal();
        });
    };
    
    // --- EVENT LISTENERS ---
    
    // Navigation
    const navigateTo = (pageId: string) => {
        pages.forEach(page => page.classList.toggle('active', page.id === pageId));
        navButtons.forEach(btn => btn.classList.toggle('active', btn.dataset.target === pageId));
        if(pageId === 'me') renderMePage();
        if(pageId === 'stats') renderStatsPage();
        if(pageId === 'skills') renderSkillsPage();
        if(pageId === 'tasks') renderTasksPage();
        if(pageId === 'calendar') renderCalendar();
    };

    navButtons.forEach(button => {
        button.addEventListener('click', () => {
            const target = button.dataset.target;
            if (target) navigateTo(target);
        });
    });

    // Task page sub-navigation
    subNavButtons.forEach(button => {
        button.addEventListener('click', () => {
            subNavButtons.forEach(btn => btn.classList.remove('active'));
            taskListContainers.forEach(container => container.classList.remove('active'));
            button.classList.add('active');
            const targetId = button.dataset.target;
            if(targetId) document.getElementById(targetId)?.classList.add('active');
        });
    });

    // Generic Add/Edit buttons
    document.body.addEventListener('click', (e) => {
        const target = e.target as HTMLElement;
        const addBtn = target.closest<HTMLElement>('.add-btn');
        const editBtn = target.closest<HTMLElement>('.edit-btn');
        if (addBtn) {
            const section = addBtn.dataset.section;
            switch(section) {
                case 'core-stats': showFormModal('core-stat'); break;
                case 'secondary-attributes': showFormModal('secondary-attribute'); break;
                case 'skills': showFormModal('skill'); break;
                case 'achievements': showFormModal('achievement'); break;
                case 'bento': showFormModal('bento'); break;
            }
        } else if (editBtn) {
             const section = editBtn.dataset.section;
             switch(section) {
                 case 'description': showFormModal('description', userProfile.description); break;
                 case 'philosophy': showFormModal('philosophy', userProfile.philosophy); break;
             }
        }
    });

    // FAB
    addTaskFab?.addEventListener('click', () => {
        const activeTab = document.querySelector<HTMLButtonElement>('.sub-nav-btn.active')?.dataset.target;
        let formType = 'daily-task';
        if (activeTab === 'weekly-tasks') formType = 'weekly-task';
        else if (activeTab === 'quests-tasks') formType = 'quest-task';
        showFormModal(formType);
    });

    // Modal Cancel
    formModalCancel?.addEventListener('click', hideFormModal);
    
    // Theme Management
    const applyTheme = (theme: 'light' | 'dark') => {
        document.body.dataset.theme = theme;
        localStorage.setItem('theme', theme);
        if (darkModeToggle) darkModeToggle.checked = theme === 'dark';
    };
    darkModeToggle?.addEventListener('change', () => applyTheme(darkModeToggle.checked ? 'dark' : 'light'));

    // Settings Modal
    settingsBtn?.addEventListener('click', () => settingsModal?.classList.remove('hidden'));
    const closeSettingsModal = () => settingsModal?.classList.add('hidden');
    closeSettingsBtn?.addEventListener('click', closeSettingsModal);
    settingsModal?.addEventListener('click', (e) => { if (e.target === settingsModal) closeSettingsModal(); });

    // --- CALENDAR LOGIC ---
    const renderCalendar = () => {
        if (!calendarGrid || !monthYearHeader) return;
        calendarGrid.innerHTML = '';
        const year = currentDate.getFullYear();
        const month = currentDate.getMonth();
        monthYearHeader.textContent = `${currentDate.toLocaleString('default', { month: 'long' })} ${year}`;
        const firstDayOfMonth = new Date(year, month, 1).getDay();
        const daysInMonth = new Date(year, month + 1, 0).getDate();
        const today = new Date();
        const isTodayInCurrentMonth = today.getFullYear() === year && today.getMonth() === month;
        for (let i = 0; i < firstDayOfMonth; i++) calendarGrid.appendChild(document.createElement('div'));
        for (let day = 1; day <= daysInMonth; day++) {
            const dayElement = document.createElement('div');
            dayElement.textContent = day.toString();
            dayElement.classList.add('calendar-day', 'current-month');
            const dateKey = `${year}-${month + 1}-${day}`;
            dayElement.dataset.date = dateKey;
            if (isTodayInCurrentMonth && day === today.getDate()) dayElement.classList.add('today');
            
            const dayData = calendarData[dateKey];
            if (dayData && (dayData.note || dayData.checklist.length > 0)) {
                dayElement.classList.add('has-note');
            }
            if(dateKey === selectedDateKey) dayElement.classList.add('selected');
            dayElement.addEventListener('click', () => handleDayClick(day, month, year, dayElement));
            calendarGrid.appendChild(dayElement);
        }
    };
    
    const renderCalendarChecklist = (items: ChecklistItem[]) => {
        if (!calendarChecklist) return;
        calendarChecklist.innerHTML = '';
        items.forEach(item => {
            const li = document.createElement('li');
            li.className = 'checklist-item';
            li.dataset.id = item.id;
            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.checked = item.completed;
            checkbox.addEventListener('change', () => { item.completed = checkbox.checked; renderCalendarChecklist(items); });

            const span = document.createElement('span');
            span.textContent = item.text;
            if (item.completed) span.classList.add('completed');
            
            li.appendChild(checkbox);
            li.appendChild(span);
            
            // Context Menu / Long Press
            li.addEventListener('contextmenu', e => {
                e.preventDefault();
                showContextMenu(e.clientX, e.clientY, item);
            });
            li.addEventListener('pointerdown', e => {
                longPressTimer = window.setTimeout(() => showContextMenu(e.clientX, e.clientY, item), 500);
            });
            li.addEventListener('pointerup', () => clearTimeout(longPressTimer));
            li.addEventListener('pointerleave', () => clearTimeout(longPressTimer));

            calendarChecklist.appendChild(li);
        });
    };

    const handleDayClick = (day: number, month: number, year: number, element: HTMLElement) => {
        if (selectedDayElement) selectedDayElement.classList.remove('selected');
        selectedDayElement = element;
        selectedDayElement.classList.add('selected');
        selectedDateKey = `${year}-${month + 1}-${day}`;
        if(!calendarDataModal || !calendarModalTitle || !calendarNoteInput) return;

        const dayData = calendarData[selectedDateKey] || { note: '', checklist: [] };

        calendarModalTitle.textContent = `Data for ${new Date(year, month, day).toLocaleDateString()}`;
        calendarNoteInput.value = dayData.note;
        renderCalendarChecklist(dayData.checklist);

        calendarDataModal.classList.remove('hidden');
        addChecklistItemInput.focus();
    };
    const closeCalendarDataModal = () => {
        calendarDataModal?.classList.add('hidden');
        if (selectedDayElement) { selectedDayElement.classList.remove('selected'); selectedDayElement = null; }
        selectedDateKey = null;
    };
    const handleSaveCalendarData = () => {
        if (selectedDateKey && calendarNoteInput) {
            const noteText = calendarNoteInput.value.trim();
            const dayData = calendarData[selectedDateKey] || { note: '', checklist: [] };
            dayData.note = noteText;
            
            if (!dayData.note && dayData.checklist.length === 0) {
                delete calendarData[selectedDateKey];
            } else {
                calendarData[selectedDateKey] = dayData;
            }
            saveData();
        }
        closeCalendarDataModal();
        renderCalendar();
    };

    const handleAddChecklistItem = () => {
        if (!selectedDateKey || !addChecklistItemInput) return;
        const text = addChecklistItemInput.value.trim();
        if (!text) return;
        
        if (!calendarData[selectedDateKey]) {
            calendarData[selectedDateKey] = { note: '', checklist: [] };
        }
        const newItem: ChecklistItem = { id: Date.now().toString(), text, completed: false };
        calendarData[selectedDateKey].checklist.push(newItem);
        
        renderCalendarChecklist(calendarData[selectedDateKey].checklist);
        addChecklistItemInput.value = '';
        addChecklistItemInput.focus();
    };

    // Context Menu Logic
    const showContextMenu = (x: number, y: number, item: ChecklistItem) => {
        if (!contextMenu) return;
        contextMenu.innerHTML = '';
        contextMenu.classList.remove('hidden');
        contextMenu.style.top = `${y}px`;
        contextMenu.style.left = `${x}px`;

        const menuItem = document.createElement('div');
        menuItem.className = 'context-menu-item';
        menuItem.textContent = 'Add as a quest';
        menuItem.onclick = () => {
            const newQuest: Task = {
                id: Date.now().toString(),
                name: item.text,
                playerXp: 50, // Default XP
                attributeRewards: [],
                coreStatXpRewards: [],
                skillRewards: [],
                completed: false
            };
            quests.push(newQuest);
            saveData();
            renderTasksPage(); // or renderAll()
            hideContextMenu();
        };
        contextMenu.appendChild(menuItem);
    };

    const hideContextMenu = () => {
        contextMenu?.classList.add('hidden');
    };

    document.addEventListener('click', hideContextMenu);
    prevMonthButton?.addEventListener('click', () => { currentDate.setMonth(currentDate.getMonth() - 1); renderCalendar(); });
    nextMonthButton?.addEventListener('click', () => { currentDate.setMonth(currentDate.getMonth() + 1); renderCalendar(); });
    saveCalendarDataButton?.addEventListener('click', handleSaveCalendarData);
    cancelCalendarDataButton?.addEventListener('click', closeCalendarDataModal);
    calendarDataModal?.addEventListener('click', (e) => { if (e.target === calendarDataModal) closeCalendarDataModal(); });
    addChecklistItemBtn?.addEventListener('click', handleAddChecklistItem);
    addChecklistItemInput?.addEventListener('keydown', (e) => { if(e.key === 'Enter') handleAddChecklistItem(); });
    
    // --- INITIALIZATION ---
    const renderAll = () => {
        const activePage = document.querySelector('.page.active')?.id || 'me';
        navigateTo(activePage);
    };
    
    loadData();
    handleTaskResets();
    saveData(); // Save in case resets happened
    
    // Set theme. Priority: 1. Saved in localStorage, 2. Default to dark.
    const savedTheme = localStorage.getItem('theme') as 'light' | 'dark' | null;
    applyTheme(savedTheme || 'dark');
    
    navigateTo('me');
});
